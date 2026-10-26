# n8n에서 키트 실행하기

`mock-pipeline.json`을 Import from File로 가져오면 Schedule Trigger → Execute Command 두 개가 연결돼요. 흐름·관문·승인·재개는 Python 키트가 처리해요. 워크플로는 꺼진 상태이고 유료 키를 포함하지 않아요.

1. 본인만 사용하는 셀프 호스팅 n8n 실행 환경에 Python 키트를 설치해요.
2. 두 Execute Command 노드의 `/opt/auto-kit/`를 실제 경로로 바꿔요. Docker이면 명령은 호스트가 아닌 n8n 컨테이너 안에서 실행돼요.
3. 수동 실행해 `dry_run` 결과와 Python 대시보드를 확인해요. 이렇게 보이면 성공: 두 노드 완료, 카드/MP4가 `private/state/`에 생겨요.
4. 시간대를 확인하고 워크플로를 켜요. 실제 전환은 먼저 Python README의 키·권리·인증·상한 설정을 끝낸 뒤 해요.

> 확인할 점: Execute Command는 n8n Cloud에서 제공되지 않으며 n8n 2.0부터 기본 비활성화돼요. 본인만 관리하는 셀프 호스팅에서 노드 허용 설정을 직접 검토하세요. 워크플로 안에 키나 외부에서 입력받은 셸 문자열을 넣지 마세요. [공식 노드 안내](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executecommand/) · [조사 노트](../../../research-advanced/nocode.md)
