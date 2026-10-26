---
name: guidebook-research
description: Use when a guidebook phase asks you (Codex) to run research through Hermes, verify sources, and write research notes, SOURCES.md and FACT-SHEET.md entries.
metadata:
  version: '1.0.0'
---
# 교과서 자료조사 (Codex 담당)

2026-10-26 ReelsBook 제작의 시행착오를 반영했다. 조사 질문은 학습자 질문에서 출발한다(guidebook-writing 참고).

## Hermes 호출 (복사해서 사용)

```bash
RUN=/home/yonghun/project/hermes-research/output/<book>-research-<YYYYMMDD>
# 질의 파일: $RUN/queries/<topic>.txt  (컨테이너 경로는 /output/<book>-research-<YYYYMMDD>/...)
cd /home/yonghun/project/hermes-research && timeout 900 docker compose exec -T --user 1000:1000 -e HOME=/opt/data hermes \
  /opt/hermes/.venv/bin/hermes chat --query-file /output/<book>-research-<YYYYMMDD>/queries/<topic>.txt \
  -Q --provider openai-codex -t web -s guidebook-research --max-turns 40 > $RUN/raw/<topic>.md 2>&1
```

- `-s guidebook-research`가 Hermes 쪽 답변 형식(한국어, URL+날짜, 공식 우선, 한국 가용성, 미확인·상충 표시, 절차형 형식)을 로드한다. 질의 파일에는 **구체 질문 목록**만 쓰면 된다.
- 최대 4개 병렬. 질의 수 상한은 Phase 지시를 따른다. 실패 질의는 1회만 재시도한다.
- 컨테이너가 없으면 멈추고 보고한다. 직접 기동·재시작하지 않는다. hermes-research의 코드·config·runtime은 수정하지 않는다.

## 품질 점검 (반드시)

1. **exit 0은 성공이 아니다.** 원응답에서 `403`, `timeout`, `blocked`, "검색 실패" 표시를 grep해서 세고, 근거 URL이 실제로 붙었는지 확인한다. 2026-10-26 이전에는 검색 공급자가 프록시에서 차단되어 원응답 52개 중 47개가 근거 없이 끝났다(현재 해제됨). 실패 비율을 결과 문서에 적는다.
2. Hermes 검색이 실패하면 **Codex 내장 웹 검색(`--search`로 실행되어 있음)**과 직접 열람(curl/urllib)으로 보완하고, Hermes 근거와 Codex 직접 확인을 구분해 표시한다.
3. 핵심 공식 출처는 Codex가 직접 열어 확인한다(Phase 지시의 최소 개수). 로그인 셸·제목만 반환한 HTTP 200은 "본문 확인"으로 치지 않는다.
4. 같은 수치가 출처마다 다르면 "상충"으로 남기되, 교과서용으로 **권장 결론**("안전하게 50건으로 잡는다")을 함께 제안한다.
5. 숫자가 필요한 학습자 질문(얼마, 몇 명, 몇 %)에는 근거 있는 숫자를 끝까지 찾는다. 국내 자료가 없으면 해외 자료를 "해외 참고"로, 그것도 없으면 "학습자가 직접 확인할 위치"를 찾는다.

## 산출물 형식

- `research/<topic>.md`: 머리에 원응답 경로·SHA256. 절: 핵심 사실(각주) / 수치 표 / 한국 가용성 / 불확실·상충(+권장 결론) / 교과서 반영 포인트(장 번호).
- `research/SOURCES.md`: 번호(S###), 제목, URL, 기관, 게시·갱신일, 접근일, 신뢰도 A/B/C, 확인 수준(직접 본문 확인 / Hermes 근거 / 메타데이터만).
- `research/FACT-SHEET.md`: 사실 ID(주제 접두어-번호), 문장, 출처 번호, 반영 장, 확인 결과. **사실 ID는 연구 문서용이며 교과서 본문에 노출하지 않는다.**
- 원응답 전문은 공개 저장소에 복사하지 않는다(hermes-research/output에만). 저장소에는 경로·해시만 둔다.
- 결과 문서에 질의별 시작·종료·exit·바이트·실패 표시 수를 표로 남긴다.
