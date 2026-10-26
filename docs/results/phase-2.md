# Phase 2 결과 — 참고 사이트 분석

1. 2026-10-26, `rea` MCP 도구 207개와 브라우저·프런트엔드용 후보를 확인했다.
2. 사용을 시도한 REA 도구는 `list_browser_targets`이며, `MCP tool call requires approval, but approval policy is never`로 실행 전 차단되어 REA Evidence는 얻지 못했다.
3. 승인·MCP 설정을 바꾸지 않고 curl·Node 22·로컬 Chromium CDP로 보완했으며, 원본·JSON·스크린샷은 저장소 밖 mktemp 디렉터리에만 두었다.
4. 표지·overview·value·chroma·lab·glossary를 화면/DOM으로 보고 light도 정적으로 교차 확인했으며, 상세 근거·수치·적용/비적용 사항은 [reference-analysis.md](../reference-analysis.md)에 기록했다.
5. 장 데이터와 전체 메뉴·현재 부·장내 목차·이전/다음 이동은 참고하되, 실제 장 흐름은 개념 절의 반복이며 ReelsBook의 고정 9단계와 구별했다.
6. 체험은 Canvas 중심/설명은 SVG였고, 드래그·슬라이더·보조 토글·실패 프리셋의 입력/수치 반응을 확인했으며 키보드 대체 조작을 적용 과제로 정리했다.
7. 퀴즈는 첫 선택 즉시 보기 잠금·정답/해설 표시, 진행 막대는 학습 완료율이 아닌 스크롤 위치였고, 용어 검색·분류·종합 점수 갱신도 확인했다.
8. 시스템/수동 다크 모드·테마 저장·견본 색 유지와 6페이지375px/lab360px의 문서 가로 넘침 없음을 확인했으며, 실기기 전체 터치 검증은 하지 않았다.
9. 본문 최대880px·17px/1.75 등 실제 수치와 파일 크기·동적 의존성을 기록했고, print에서 도구가 남는 점·모든 장을 받는 검색 비용은 그대로 따르지 않기로 제안했다.
10. Phase 2 문서 두 개만 작성했으며 커밋·push·PROJECT_STATE.md 수정·다음 Phase 구현은 하지 않았다. 남은 제한은 REA 호출 차단과 미실시 실기기/PDF/냉시작 성능 검증이다.
