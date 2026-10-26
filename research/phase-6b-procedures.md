# 초보자 실습 절차 보완 근거

확인일: 2026-10-26. 공식 문서 본문을 웹 도구로 직접 확인했다. 문서 확인은 실제 Windows/macOS 앱 조작·계정 생성·OS 예약 실행을 뜻하지 않는다. 출처 목록·사실표 등록은 통합 담당자가 맡는다.

| 출처 | 공식 URL | 확인한 내용과 원고 반영 |
| --- | --- | --- |
| S259 | https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository | 웹의 새 저장소 → 소유자·이름·공개 범위 → README 추가 → 생성 순서. 실습 8에서 README와 기본 branch를 확인한 뒤 업로드하도록 연결했다. |
| S260 | https://www.audacityteam.org/manual/getting-started/make-your-first-recording/ | 빨간 녹음 버튼, 정지, 재생 확인 순서를 안내한다. 실습 5에서 본인 대본 녹음에 사용한다. 연결된 마이크 안내 https://www.audacityteam.org/manual/getting-started/connect-your-microphone/ 는 Audio setup에서 입력 기기·채널 선택을 설명한다. |
| S261 | https://www.audacityteam.org/manual/getting-started/export-your-audio/ | File → Export audio에서 파일명·위치·형식을 고른다. 실습은 WAV로 내보내며 프로젝트 저장과 오디오 파일을 구분한다. |
| S262 | https://www.audacityteam.org/features/trim/ | 파형에서 남길 부분 선택 → Edit → Remove Special → Trim Audio → 내보내기. 실습의 앞뒤 무음 제거 경로다. |
| S263 | https://ffmpeg.org/ffmpeg.html | -i 입력과 출력 파일을 사용해 내용을 재인코딩한다. 실습은 키트 설치 FFmpeg를 호출해 M4A를 PCM WAV로 변환한다. 확장자만 바꾸지 않는다. |
| S264 | https://support.apple.com/en-gb/guide/textedit/txtee6663a0e/1.20/mac/26 | Format → Make Plain Text, 저장 위치·이름 지정, 서식 제거를 확인했다. 일반 텍스트로 바꾼 뒤 확장자와 위치를 확인한다. |
| S265 | https://support.microsoft.com/en-us/windows/experience/storage-filemanagement/common-file-name-extensions-in-windows | Explorer의 View → Show → File name extensions를 켠다. 확장자 변경은 내용 변환이 아니라는 설명도 확인했다. |
| S266 | https://support.apple.com/en-gb/guide/textedit/txted1063/1.20/mac/26 | TextEdit → Settings → Open and Save의 .txt 자동 추가·일반 텍스트 인코딩 설정, 스마트 따옴표 설정을 확인했다. |
| S267 | https://blogs.windows.com/windows-insider/2018/12/10/announcing-windows-10-insider-preview-build-18298/ | 메모장 UTF-8 저장 옵션과 상태 표시를 설명한다. 본문은 새 문서 저장 시 UTF-8을 직접 고르게 한다. 과거 빌드 설명을 최신 UI 전체의 근거로 확대하지 않는다. |

## 연결된 기존 근거

- 토큰 발급·계정 확인 GET·만료 설명은 기존 S177·S030·S174를 유지한다. 새 token_check.py는 토큰 숨김 입력 후 본인 계정 ID·이름만 출력한다. 토큰 만료일이나 게시 권한을 확인하는 기능으로 설명하지 않는다.
- 예약 문법과 OS 명령 근거는 통합 담당자가 등록하는 S268~S270을 사용한다. 실습은 도우미 출력 → 사용자가 등록 → 수동 실행 → 다음 날 폴더 확인 → 사람 검수·승인 → 앱/API 게시 순서다.
- 프로필 수정 도움말 https://help.instagram.com/583107688369069 는 직접 열람 429였다. 실습 1은 ‘보통 프로필 → 프로필 편집’이라는 화면 후보와 공식 확인 링크를 제공한다. 구체 글자 수·변경 횟수 제한은 추가하지 않았다.

## 검증 한계

앱 녹음·내보내기 UI, OS 예약 등록, 다음 날 실제 예약 동작, 실계정 토큰·게시·GitHub 계정 생성은 수행하지 않았다. 파일 생성·변환·드라이런 명령은 별도의 깨끗한 임시 복사본에서 확인하며 결과는 통합 결과 문서에 남긴다.
