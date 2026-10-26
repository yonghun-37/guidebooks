# 샘플 읽기

가상 블로그 ‘퇴근 후 생활 정보’의 글 **‘2025 청년내일저축계좌, 대상과 신청 기간 정리’**예요. 논산시의 2025년 모집 공지를 직접 대조한 학습용 글이에요. 접수 기간이 끝났으므로 현재 신청 안내로 쓰지 않아요. 신청·수령 체험은 만들지 않아요. [세 경로](routes.md)의 제목·메모·사진 파일명을 이어 씁니다.

- `article.md`: 원본 Markdown. 본인 경험·출처로 바꿔 쓰세요.
- `support-check.svg`: 직접 그린 공고 점검 순서도. 실제 기관 화면·로고·생성 사진이 아니에요.
- `brief.md`: 같은 키워드의 복사용 프롬프트 묶음.
- `rendered/editor.html`: 편집기에 옮길 HTML 조각.
- `rendered/preview.html`: 로컬 브라우저로 여는 모바일 미리보기.
- `rendered/report.md`: 자동 점검 리포트.
- `rendered/REVIEW.md`: 미승인 검수표. 승인 파일·인증 정보는 동봉하지 않아요.

재생성은 키트 폴더에서 `python brief.py --notes samples/info-notes.txt --output samples/brief.md`, `python render.py samples/article.md --output samples/rendered`로 해요. 각각 `프롬프트 생성 완료:`, `HTML 생성 완료:`와 `검수 대기:`가 보이면 성공이에요. 샘플은 드라이런 연습에만 쓰고 실제 계정으로 보내지 마세요.
