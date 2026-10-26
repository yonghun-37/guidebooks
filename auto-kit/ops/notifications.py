"""알림은 먼저 로컬 파일에 남긴다. Discord는 알림, Telegram은 선택적 승인."""
import json
from pathlib import Path
from common import save_json, secrets
from transport import HTTP, https_url

def notify(run, event, *, live=False, http=None, values=None):
    reasons = [reason for result in run.get('gates', {}).values() for reason in result.get('reasons', [])]
    message = f"[{event}] {run['id']} · {run['flow']} · {run['status']}\n" + '\n'.join(reasons[:6])
    message += f"\n생성비 ${run.get('generation_cost', 0):.6f} · 미리보기 첨부/로컬 preview.html"
    local = {'event': event, 'id': run['id'], 'status': run['status'], 'message': message, 'preview': 'preview.html', 'binding': run.get('binding'), 'cost_usd': run.get('generation_cost', 0)}
    save_json(Path(run['output']) / 'notification.json', local)
    if not live:
        return local
    values, http = values if values is not None else secrets(), http or HTTP()
    preview = next((Path(f) for f in run.get('files', []) if Path(f).suffix == '.jpg'), None)
    if preview is None:
        preview = next(iter(sorted((Path(run['output']) / 'frames').glob('scene-*.png'))), None)
    failures = []
    if values.get('DISCORD_WEBHOOK_URL'):
        from urllib.parse import urlsplit
        url = values['DISCORD_WEBHOOK_URL']
        https_url(url, {'discord.com', 'discordapp.com'})
        if not urlsplit(url).path.startswith('/api/webhooks/'):
            raise ValueError('Discord incoming webhook URL을 확인하세요.')
        body = {'content': message[:1900], 'allowed_mentions': {'parse': []}}
        attachment_name='preview.png' if preview and preview.suffix=='.png' else 'preview.jpg'
        if preview:
            body['embeds'] = [{'title': '게시 전 미리보기', 'image': {'url': 'attachment://'+attachment_name}}]
        try:
            if preview:
                with preview.open('rb') as stream:
                    response = http.request('POST', url, data={'payload_json': json.dumps(body, ensure_ascii=False)}, files={'files[0]': (attachment_name, stream, 'image/jpeg' if preview.suffix == '.jpg' else 'image/png')})
            else:
                response = http.request('POST', url, json=body)
            if response.status_code not in (200, 204): failures.append('Discord')
        except ValueError:
            failures.append('Discord')
    if values.get('TELEGRAM_BOT_TOKEN') and values.get('TELEGRAM_CHAT_ID'):
        base = 'https://api.telegram.org/bot' + values['TELEGRAM_BOT_TOKEN']
        chat = values['TELEGRAM_CHAT_ID']
        payload = {'chat_id': chat, 'text': message[:3000]}
        if run['status'] in ('waiting_approval', 'scheduled'):
            b = run.get('binding', '')[:12]
            buttons = [] if run['status'] != 'waiting_approval' else [{'text': '승인', 'callback_data': f'a:{run["id"]}:{b}'}]
            buttons.append({'text': '거부', 'callback_data': f'r:{run["id"]}:{b}'})
            payload['reply_markup'] = {'inline_keyboard': [buttons]}
        try:
            if preview:
                with preview.open('rb') as stream:
                    response=http.request('POST', base + '/sendPhoto', data={'chat_id': chat, 'caption': '미리보기 ' + run['id']}, files={'photo': (preview.name, stream)})
                    if response.status_code!=200:failures.append('Telegram preview')
            http.json('POST', base + '/sendMessage', json=payload)
        except ValueError:
            failures.append('Telegram')
    if failures:
        local['delivery_failed'] = failures
        save_json(Path(run['output']) / 'notification.json', local)
    return local

def poll(pipeline, *, http=None, values=None):
    values, http = values if values is not None else secrets(), http or HTTP()
    token = values.get('TELEGRAM_BOT_TOKEN')
    user, chat = values.get('TELEGRAM_ALLOWED_USER'), values.get('TELEGRAM_CHAT_ID')
    if not token or not user or not chat:
        raise ValueError('Telegram bot token·허용 사용자 ID·chat ID를 모두 설정하세요.')
    base = 'https://api.telegram.org/bot' + token
    offset = pipeline.store.kv('telegram_offset') or 0
    updates = http.json('GET', base + '/getUpdates', params={'offset': offset, 'timeout': 25, 'allowed_updates': '["callback_query"]'}).get('result', [])
    for update in updates:
        if update['update_id'] < offset: continue
        callback = update.get('callback_query', {})
        allowed = str(callback.get('from', {}).get('id')) == user and str(callback.get('message', {}).get('chat', {}).get('id')) == chat
        response = '허용되지 않은 요청'
        if allowed:
            fields = callback.get('data', '').split(':')
            if len(fields) == 3 and fields[0] in ('a', 'r'):
                try:
                    run = pipeline.store.get(fields[1])
                    if run.get('binding', '')[:12] == fields[2]:
                        if fields[0] == 'a': pipeline.approve(run['id'], actor='telegram:' + user)
                        else: pipeline.reject(run['id'])
                        response = '처리 완료'
                except ValueError:
                    response = '상태·해시·공개 시각 확인 필요'
        if callback.get('id'):
            http.json('POST', base + '/answerCallbackQuery', json={'callback_query_id': callback['id'], 'text': response})
        offset = update['update_id'] + 1
        pipeline.store.kv('telegram_offset', offset)
    return len(updates)
