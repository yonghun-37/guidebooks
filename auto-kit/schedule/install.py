"""starter-kit/schedule_setup.py의 절대경로·인용 방식을 확장한다."""
import argparse
from pathlib import Path
import plistlib
import re
import shlex
from subprocess import list2cmdline
import sys
from common import ROOT, cli, kit_path

def generate(os_name, time, flow, destination, *, python=None, config=None, state=None, live=False):
    if not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d',time): raise ValueError('시각은 HH:MM 형식으로 쓰세요.')
    python=str(python or sys.executable)
    if not Path(python).is_absolute(): raise ValueError('Python은 절대 경로를 지정하세요.')
    destination=Path(destination).resolve();destination.mkdir(parents=True,exist_ok=True)
    config=kit_path(config or 'config.example.json');state=kit_path(state or 'private/state')
    args=[python,str(ROOT/'pipeline.py'),'tick','--flow',flow,'--daily-at',time,'--config',str(config),'--state',str(state)]
    if live: args.append('--live')
    for value in args:
        if any(ord(c)<32 for c in value): raise ValueError('예약 인수에 줄바꿈·제어 문자를 넣지 마세요.')
    hour,minute=map(int,time.split(':'));minutes=sorted((minute+n*15)%60 for n in range(4))
    label='org.guidebooks.auto-kit.'+flow
    if os_name=='windows':
        def ps(value): return "'"+value.replace("'","''")+"'"
        # Register-ScheduledTask는 프로그램/인수를 분리하고 cmd.exe를 거치지 않는다.
        path=destination/f'install-{flow}.ps1'
        script=f'''$ErrorActionPreference = 'Stop'
$action = New-ScheduledTaskAction -Execute {ps(python)} -Argument {ps(list2cmdline(args[1:]))} -WorkingDirectory {ps(str(ROOT))}
$trigger = New-ScheduledTaskTrigger -Once -At {ps(time)} -RepetitionInterval (New-TimeSpan -Minutes 15)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName {ps(label)} -Action $action -Trigger $trigger -Settings $settings -Description 'auto-kit tick · 15분마다 상태 확인'
Get-ScheduledTask -TaskName {ps(label)}
# 해제: Unregister-ScheduledTask -TaskName {ps(label)}
'''
        path.write_text(script,encoding='utf-8-sig')
        instruction=f'PowerShell: & "{path}" · 확인: Get-ScheduledTask -TaskName {label}'
    elif os_name=='macos':
        path=destination/f'{label}.plist'
        data={'Label':label,'ProgramArguments':args,'WorkingDirectory':str(ROOT),'StartCalendarInterval':[{'Hour':h,'Minute':m} for h in range(24) for m in minutes],'StandardOutPath':str(state/'schedule.log'),'StandardErrorPath':str(state/'schedule-error.log')}
        path.write_bytes(plistlib.dumps(data,sort_keys=False))
        installer=destination/f'install-{flow}-macos.sh'
        quoted=shlex.quote(str(path))
        installer.write_text('#!/bin/sh\nset -eu\nmkdir -p "$HOME/Library/LaunchAgents"\ncp '+quoted+' "$HOME/Library/LaunchAgents/'+label+'.plist"\nlaunchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/'+label+'.plist"\n# 해제: launchctl bootout "gui/$(id -u)/'+label+'"\n',encoding='utf-8')
        instruction=f'sh {shlex.quote(str(installer))} · 확인: launchctl print "gui/$(id -u)/{label}"'
    elif os_name=='cron':
        path=destination/f'install-{flow}-cron.sh'
        line=','.join(map(str,minutes))+' * * * * '+shlex.join(args).replace('%',r'\%')+' >> '+shlex.quote(str(state/'schedule.log')).replace('%',r'\%')+' 2>&1 # '+label
        path.write_text('#!/bin/sh\nset -eu\nmkdir -p '+shlex.quote(str(state))+'\n# 같은 이름이 이미 있으면 등록하지 않는다. 다른 예약은 유지한다.\nexisting=$(crontab -l 2>/dev/null || true)\nif printf "%s\\n" "$existing" | grep -Fq '+shlex.quote(label)+'; then echo "이미 등록됨"; exit 1; fi\n{ printf "%s\\n" "$existing"; printf "%s\\n" '+shlex.quote(line)+'; } | crontab -\ncrontab -l\n# 해제: crontab -e에서 '+label+' 줄만 삭제\n',encoding='utf-8')
        instruction='sh '+shlex.quote(str(path))+' · 확인: crontab -l'
    else: raise ValueError('os는 windows/macos/cron 중 하나를 고르세요.')
    state.mkdir(parents=True,exist_ok=True)
    return {'path':str(path),'instructions':instruction,'note':'OS 현지 시각. 15분마다 재개/예약 발행, 지정 시각 이후 하루 1회 새 생성. PC 켜짐·로그인/절전 확인.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--os',choices=['windows','macos','cron'],required=True);p.add_argument('--time',default='09:17');p.add_argument('--flow',choices=['insta','shorts'],required=True);p.add_argument('--dest',default='private/schedule');p.add_argument('--python',default=sys.executable);p.add_argument('--config');p.add_argument('--state');p.add_argument('--live',action='store_true')
    a=p.parse_args();r=generate(a.os,a.time,a.flow,kit_path(a.dest),python=a.python,config=a.config,state=a.state,live=a.live)
    print('예약 파일 생성 완료: '+r['path']);print(r['instructions']);print(r['note'])

if __name__=='__main__': cli(main)
