"""GitHub 입력을 셸에 삽입하지 않고 검증해 실행한다."""
import os
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import load_config, kit_path, cli
from pipeline import Pipeline
from ops.report import report

def main():
    action=os.environ.get('KIT_ACTION') or 'tick'
    identifier=os.environ.get('KIT_RUN_ID','')
    flow=os.environ.get('KIT_FLOW') or 'insta'
    live=os.environ.get('KIT_LIVE','false')=='true'
    if flow not in ('insta','shorts') or action not in ('tick','approve','reject','resume','report'):
        raise ValueError('허용되지 않은 workflow 입력입니다.')
    if action in ('approve','reject','resume') and not re.fullmatch('[0-9a-f]{12}',identifier):
        raise ValueError('실행 ID는 12자리 소문자 16진수입니다.')
    p=Pipeline(load_config(kit_path('config.json')) if kit_path('config.json').exists() else load_config())
    if action=='tick': p.tick(flow=flow,live=live,daily_at='09:17')
    elif action=='approve': p.approve(identifier);p.resume(identifier,live=live)
    elif action=='reject': p.reject(identifier)
    elif action=='resume': p.resume(identifier,live=live)
    else: report(p.store,p.config)
    print('작업 종료. 상태는 다음 암호화 저장 단계에서 보존됩니다.')

if __name__=='__main__':cli(main)
