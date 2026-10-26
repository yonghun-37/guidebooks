from datetime import timedelta
from pathlib import Path
import pytest
from common import now, load_config, read_json, save_json
from pipeline import Pipeline
from providers import Provider
from state import Store
from publish.youtube import metadata

def test_expired_approval_returns_to_review(tmp_path):
    p=Pipeline(load_config(),tmp_path);r=p.run('insta');p.approve(r['id'])
    r=p.store.get(r['id']);r['approval']['expires_at']=(now()-timedelta(seconds=1)).isoformat()
    save_json(Path(r['output'])/'APPROVED.json',r['approval']);p.store.save(r)
    result=p.resume(r['id'])
    assert result['status']=='waiting_approval'
    p.approve(r['id'])
    assert p.resume(r['id'])['status']=='dry_run'

def test_post_review_shorts_dry_schedule_can_reject(tmp_path):
    cfg=load_config();cfg['mode']='post_review';p=Pipeline(cfg,tmp_path)
    r=p.run('shorts')
    assert r['status']=='scheduled'
    assert p.reject(r['id'])['status']=='rejected'

def test_session_resume_can_query_after_publish_time():
    cfg=load_config()['youtube'];cfg['publishAt']='2000-01-01T00:00:00Z'
    result=metadata({'title':'제목','caption':'문안'},cfg,resuming=True)
    assert result['status']['publishAt']==cfg['publishAt']

def test_partial_usage_keeps_reservation(tmp_path):
    cfg=load_config();cfg['providers']['llm']='openai';store=Store(tmp_path)
    def invoke(kind,payload,model): return {'value':Provider.mock_draft(payload['source'],'insta'),'usage':{'input_tokens':3}}
    Provider(cfg,store,'r',invoke=invoke).draft({'title':'청년 지원금 확인','text':'청년 지원금 신청 전 확인','entities':[]},'insta')
    call=store.calls()[0]
    assert call['actual']==call['reserved']

def test_tick_does_not_generate_before_local_time(tmp_path):
    p=Pipeline(load_config(),tmp_path)
    with pytest.raises(ValueError): p.tick(flow='insta',provider='mock',daily_at='99:99')
