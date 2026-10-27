너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/DESIGN-blog-advanced.md(1.1·6·8절), docs/results/phase-BX6-policy.md, docs/results/phase-BX7.md, 그리고 **docs/results/phase-BX7b-claude-bypass.py**(Claude 검수에서 만든 우회 시험 10개)를 읽어라.

이번 작업은 **Phase BX7b. 자동 발행 구조 재설계(Claude 검수 차단)**다. 수정 범위: blog-auto-kit/, site-blog/advanced/, scripts/check_blog_advanced.py·repro_blog_advanced.sh, docs/DESIGN-blog-advanced.md는 읽기만. commit하지 마라.

## 문제
BX7의 `may_auto_publish`는 자유 문장을 단어 목록으로 검사한다. Claude 시험 10개 중 5개가 사람 승인 없이 future가 됐다: 본문 안 쿠팡 제휴 링크 `[여기서 구매](https://link.coupang.com/a/abc123)`(대가성 표시 없는 상업 글 자동 발행), 영어 `fever`, 띄어 쓴 `해 열 제`, `서울 마포구 ○○어린이집`, `이 매트에서 재우면 질식 걱정이 없어요.` 단어를 더 추가하는 방식은 계속 샌다.

## 고칠 구조: "승인된 틀 + 검증된 데이터"만 자동 발행
1. **자동 발행 조건을 바꾼다**: 사람 승인 없이 예약할 수 있는 글은 **사람이 한 번 승인한 글 틀(template)에 구조화 데이터만 채워 만든 글뿐**이다. 
   - 글 틀 파일(`content/templates/<id>.md`)과 그 해시를 사람이 승인한 기록(`blog.py template approve <id> --by 서윤`)이 있어야 한다. 틀이 바뀌면 승인 무효.
   - 데이터는 JSON Schema로 검증한다: 정해진 칸만, 타입·길이·열거값(예: 그림책 주제·월령 구간은 목록에서만), 자유 문장 칸 없음, URL은 설정의 허용 도메인(공식 기관 등)만.
   - 발행 직전 `본문 == render(승인된 틀, 데이터)`를 바이트 단위로 확인한다. 하나라도 다르면 사람 승인.
   - LLM이 쓴 문장, 사람이 쓴 자유 문장, 경험·사진이 있는 글은 **어떤 설정에서도 사람 승인**이다. 단어 검사(건강·식별·상업 신호)는 남겨 두되 사람 검토 보고서의 보조 표시로 쓴다. 자동 발행 허용 근거로 쓰지 않는다.
2. **링크**: 본문·HTML의 모든 URL을 추출해, 제휴·쇼핑 도메인이면 상업 관계로 분류한다(표시 관문 + 사람 승인). 허용 목록에 없는 도메인이 있으면 사람 승인.
3. 샘플: 자동 발행 시연용으로 승인된 틀 1개를 만든다(예: "이번 달 도서관 그림책 주제 목록" — 공공 자료의 고정 칸만 채움, 건강 내용 없음). 기존 `run --sample` 등 장별 명령의 출력이 바뀌면 course/build_expected.py로 다시 만들고 본문 성공 문구를 맞춘다.
4. 테스트: phase-BX7b-claude-bypass.py의 10개를 tests/로 옮겨 모두 통과(draft 유지)시킨다. 추가로 다음을 증명한다.
   - 승인된 틀 + 유효 데이터는 auto에서 future가 된다.
   - 틀을 한 글자 바꾸거나, 데이터에 허용 밖 값·URL·긴 문자열을 넣거나, 렌더 결과를 손으로 고치면 draft로 남는다.
   - BX6·BX7 반례는 계속 통과한다.
5. 본문: A0(자동화 수준 표), A3(글 틀), A5(관문 흐름 그림), A6(발행 조건), A11(운영), A12, E2E를 새 구조로 고친다. 핵심 문장: "자동 발행은 내가 승인한 틀에 정해진 데이터만 채운 글뿐이에요. AI나 사람이 쓴 문장이 들어간 글은 전부 내가 읽고 승인해요." 단어 검사는 보조라고 정직하게 쓴다. 틀 승인 명령과 예상 출력도 본문에 넣는다.
6. 게이트: build_expected `--check`, check_blog_advanced `--check` 불일치 0, repro 통과, pytest 전체, style_lint, check_site 네 책 오류 0, 바뀐 장 브라우저 3폭×2테마, 콘솔 0. 결과 docs/results/phase-BX7b.md. `python3 scripts/notify.py "✅ [BX7b 완료] ..."`.
