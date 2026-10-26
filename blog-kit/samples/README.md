# 샘플 읽기

가상 블로그 ‘퇴근 후 생활 정보’의 글 **‘청년 직장인 지원 제도, 신청 전에 어디부터 볼까’**예요. 검색으로 찾은 공고를 내 조건과 대조하는 순서를 설명해요. 실제 제도·금액·성과를 안내하지 않아요. 수아의 경험은 가상 편집 연습임을 본문에 밝혔어요.

- `article.md`: 원본 Markdown. 본인 경험·출처로 바꿔 쓰세요.
- `support-check.svg`: 직접 그린 공고 점검 순서도. 실제 기관 화면·로고·생성 사진이 아니에요.
- `brief.md`: 같은 키워드의 복사용 프롬프트 묶음.
- `rendered/editor.html`: 편집기에 옮길 HTML 조각.
- `rendered/preview.html`: 로컬 브라우저로 여는 모바일 미리보기.
- `rendered/report.md`: 자동 점검 리포트.
- `rendered/REVIEW.md`: 미승인 검수표. 승인 파일·인증 정보는 동봉하지 않아요.

재생성은 키트 폴더에서 `python brief.py --output samples/brief.md`, `python render.py samples/article.md --output samples/rendered`로 해요. 각각 `프롬프트 생성 완료:`, `HTML 생성 완료:`와 `검수 대기:`가 보이면 성공이에요. 샘플은 드라이런 연습에만 쓰고 실제 계정으로 보내지 마세요.
