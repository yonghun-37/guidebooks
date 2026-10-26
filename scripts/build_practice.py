#!/usr/bin/env python3
"""실습 정적 원고와 동일 단계의 E2E 목록·7v 확인표·자체 도식을 생성한다."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
E = html.escape
SOURCES = {sid: dict(re.findall(r'^- ([^:]+): (.*)$', body, re.M)) for sid, body in re.findall(r'### (S\d+)\.[^\n]*\n(.*?)(?=\n<a id=|\Z)', (ROOT/'research/SOURCES.md').read_text(), re.S)}


def code(value):
    return '<div class="code-box"><pre><code>'+E(value)+'</code></pre></div>'


def official(sid, label='공식 도움말'):
    return f'<a href="{E(SOURCES[sid]["URL"], quote=True)}">{label} · {sid}</a>'


def menu(text, sid, screen):
    return f'<div class="menu-unverified" data-verify="app-menu" data-screen="{E(screen, quote=True)}"><p><strong>앱 버전에 따라 이름이 다를 수 있음 — 보통 이런 이름</strong>: {text}</p><p class="small">한국 앱 메뉴·배치 미확인. 확인일 2026-10-26. {official(sid)}에서 기능을 찾고, 다르면 OS·앱 버전·계정 유형과 화면을 기록하세요. 개인정보·인증 코드·토큰은 기록하지 마세요.</p></div>'


def step(id_, title, now, why, follow, success, errors, win=None, mac=None):
    return dict(id=id_, title=title, now=now, why=why, follow=follow, success=success, errors=errors,
                win=win or '이 단계는 Windows와 무관한 휴대폰 또는 웹 작업입니다. 휴대폰 OS와 앱 버전의 화면 차이는 공식 도움말로 확인하세요.',
                mac=mac or '이 단계는 macOS와 무관한 휴대폰 또는 웹 작업입니다. 휴대폰 OS와 앱 버전의 화면 차이는 공식 도움말로 확인하세요.')


def page(slug, title, goal, supplies, minutes, facts, sources, steps, intro=''):
    return dict(slug=slug, title=title, goal=goal, supplies=supplies, minutes=minutes, facts=facts, sources=sources, steps=steps, intro=intro)


PAGES = [
page('00-start','시작 전에','오늘의 경로와 준비물을 정한다.', 'PC, 휴대폰, 본인 이메일, 파일을 보관할 공간', '10분', 'PRAC-25', [], [
step('route','오늘의 전체 지도 읽기','실습 0~7을 오늘의 기본 경로로 고릅니다.','계정과 개발자 설정을 한꺼번에 준비하다 멈추지 않기 위해서입니다.',
'<ol><li>준비물 PC·휴대폰·본인 이메일을 놓고 약 <strong>3~4시간</strong>을 비워 둡니다. 교재의 편집상 시간 배분이며 완주 보장이 아닙니다.</li><li>아래 지도에서 <strong>계정 → 설치 → 문안 → 카드 → 릴스 → 검수 → 앱 게시</strong>를 읽습니다. 카드 또는 릴스 하나부터 게시해도 됩니다.</li><li>실습 8 API·9 예약은 선택 심화입니다. 개발자 앱·토큰·공개 URL은 실습 7 수동 게시에 필요 없습니다. 실습 10은 게시 뒤 관찰입니다.</li></ol><figure class="practice-figure"><img src="../assets/img/practice/map.svg" alt="기본 경로는 실습 0부터 7까지, 선택 심화는 8과 9, 게시 뒤 관찰은 10"><figcaption>학습 순서 도식 · 시간·진행은 독자마다 다릅니다.</figcaption></figure>',
'오늘은 본인이 검수한 첫 게시물 주소를 기록하고, 나머지 자동화는 선택한다는 목표가 정해졌습니다.',
['시간이 부족하면 카드 또는 릴스 하나를 먼저 마치고 E2E에 남은 단계를 표시하세요.','실계정이 아직 없으면 생성·검수 드라이런까지 먼저 연습할 수 있습니다.']),
step('record','진행 기록과 도움받는 법','E2E 체크리스트에서 진행 상태를 남깁니다.','어느 단계에서 막혔는지 다시 찾기 위해서입니다.',
'<ol><li><a href="e2e.html"><strong>E2E 한눈에 보기</strong></a>를 열고 이 단계를 체크해 보세요. 각 항목을 누르면 해당 절로 이동합니다.</li><li>브라우저 저장소(localStorage)는 이 브라우저 안의 작은 기록 공간입니다. 계정 동기화가 아니며 서버에 보내지 않습니다. 비밀번호·토큰은 쓰지 마세요.</li><li>막히면 해당 단계의 <strong>이렇게 보이면?</strong>을 먼저 읽습니다. 해결되지 않으면 명령·오류 문구·OS·파일 위치만 정리해 도움을 구하세요.</li></ol>',
'체크를 바꾸면 완료 수가 바뀝니다. 저장이 허용된 브라우저에서는 새로고침 뒤에도 유지됩니다.',
['저장할 수 없다고 나오면 현재 페이지에서는 계속 체크하고, 이동 전 진행을 별도 메모에 적으세요.','앱 메뉴가 다르면 단정해서 누르지 말고 해당 공식 도움말과 미확인 표시를 읽으세요.'])
], '<p>하린과 정 선배는 가상 인물입니다. 예제는 합성 자료로 연습하고, 실제 게시에는 본인이 확인한 자료를 씁니다. 이 교재의 앱 메뉴는 일부 미확인이며 실계정 게시 성공을 검증하지 않았습니다.</p>'),
page('01-account','테스트 계정과 보안 준비','본인 게시 계정을 구분하고 복구 수단을 갖춘다.', '휴대폰, 본인이 접근할 이메일/전화, 인증앱', '25분', 'PRAC-20 API-01', ['S180','S181','S182','S176'], [
step('test-account','연습용 테스트 계정 만들기','기존 계정을 쓸지 연습용 새 계정을 만들지 결정합니다.','실수한 게시물이 본계정에 올라가지 않게 대상부터 구분합니다.',
'<ol><li>본인만 관리하는 계정 이름을 정하고 실습용임을 소개에 적을 문장을 준비합니다. 실존 브랜드·인물을 사칭하지 않습니다.</li><li><strong>방법 A: 기존 계정에서 추가</strong>. 아래 탐색 후보로 새 계정 만들기를 찾고 앱이 요구하는 가입·인증을 따릅니다.</li><li><strong>방법 B: 로그아웃 상태에서 가입</strong>. 시작 화면의 새 계정 만들기에 해당하는 항목을 찾아 본인 이메일/전화로 가입합니다. 가입 필드·인증 순서는 미확인입니다.</li><li>이메일 <code>이름+연습@도메인</code> 같은 <strong>+ 별칭 팁</strong>은 메일 서비스의 별칭 지원과 Instagram의 수락 여부를 먼저 확인해야 하는 후보입니다. 7r에는 성공 근거가 없으므로 필수 경로로 쓰지 않습니다. 안 되면 본인이 관리하는 별도 이메일을 쓰세요.</li><li>대상 사용자 이름을 별도 개인 메모에 기록합니다. 비밀번호는 이 교재에 입력하지 않습니다.</li></ol>'+
menu('<strong>계정 추가 / Add account → 새 계정 만들기 / Create new account</strong> 또는 로그아웃 시작 화면의 <strong>가입 / Sign up</strong>. 두 방법의 현행 한국 가입 순서는 확인 필요입니다. S180은 전환 도움말이며 가입 경로를 입증하지 않습니다.', 'S180','기존 계정 추가·로그아웃 가입·이메일 별칭'),
'사용자 본인이 가입과 인증을 마친 뒤, 프로필의 사용자 이름이 의도한 연습 계정인지 확인했습니다. 작업자가 가입 성공을 검증한 것은 아닙니다.',
['인증이 막히면 반복 생성하지 말고 본인 연락처·앱 도움말을 확인하세요.','+ 별칭이 거부되면 지원된다고 가정하지 말고 본인 별도 주소로 확인하세요.']),
step('professional','계정 유형과 공개 범위 확인','필요하면 연습 계정을 크리에이터 또는 비즈니스로 전환합니다.','API는 프로페셔널 계정을 대상으로 하므로 경로를 미리 구분합니다.',
'<ol><li>프로필 사용자 이름을 먼저 확인하고 아래 메뉴 후보를 찾습니다.</li><li>앱이 제시하는 카테고리·<strong>크리에이터 / Creator</strong> 또는 <strong>비즈니스 / Business</strong> 선택·공개 안내를 읽습니다. 이 교재는 크리에이터를 탐색 예로 듭니다.</li><li>전환 뒤 실제 계정 유형·공개 상태를 확인합니다. Instagram Login API에는 Facebook 페이지 연결이 필수라는 안내를 붙이지 않습니다(API-01).</li></ol>'+
menu('<strong>프로필 → 메뉴 → 설정 및 활동 / Settings and activity → 계정 유형 및 도구 / Account type and tools → 프로페셔널 계정으로 전환 / Switch to professional account</strong>. 카테고리·유형·공개 동의 화면의 순서도 미확인입니다.', 'S180','프로페셔널 전환·크리에이터 선택·공개 동의'),
'본인이 계정 유형과 공개 안내를 확인해 개인 메모에 적었습니다. 메뉴가 없으면 확인을 보류한 상태로 남깁니다.',
['이미 전환한 계정인지 먼저 확인하세요. 메뉴 부재만으로 한국 전체 비지원이라고 판단하지 않습니다.','전환 과정에 유료 구독 화면이 나오면 필수 단계라고 생각하지 말고 도움말로 돌아가세요.']),
step('security','2단계 인증과 복구 수단','인증앱과 백업 수단을 준비합니다.','비밀번호 하나만 유출되어 계정을 잃는 위험을 줄이기 위해서입니다.',
'<ol><li>2단계 인증은 비밀번호 외에 인증 코드를 더 확인하는 로그인 보호입니다. 아래 후보에서 <strong>대상 계정</strong>을 선택합니다.</li><li>공식 도움말과 앱 안내에 따라 인증앱 연결·확인 코드를 입력합니다. 설정 키·QR·코드는 남에게 보여 주지 마세요.</li><li>백업 코드는 인증앱을 잃었을 때 사용할 복구용 코드입니다. 발급 방법을 확인하고 본인만 접근하는 곳에 보관합니다. 이메일/전화 복구 연락처에도 접근 가능한지 확인합니다.</li></ol>'+
menu('<strong>계정 센터 / Accounts Center → 비밀번호 및 보안 / Password and security → 2단계 인증 / Two-factor authentication → 대상 계정 → 인증 앱 / Authentication app</strong>. 연결·완료 화면 미확인입니다.', 'S181','인증앱 2단계 인증')+
menu('<strong>2단계 인증 → 백업 코드 / Backup codes</strong>에 해당하는 항목. 발급·재발급 버튼과 코드 개수는 확인 필요입니다.', 'S182','백업코드 발급·보관'),
'대상 계정에서 2단계 인증 완료 표시를 본인이 확인하고 복구 연락처와 백업 수단을 안전하게 보관했습니다.',
['코드가 틀리면 인증앱의 대상 계정과 기기 시간을 점검하고 앱 도움말을 따르세요.','백업 코드 화면을 찾지 못했다면 완료로 체크하지 말고 도움말로 확인하세요.']),
step('developer','API 실습 준비물만 구분','API를 선택할 때 필요한 준비물을 적습니다.','오늘 앱 첫 게시를 개발자 설정 때문에 미루지 않기 위해서입니다.',
'<ol><li>API는 프로그램이 서비스에 요청을 보내는 통로입니다. 실습 8을 할 때만 Meta 개발자 계정·앱, 본인 공개 프로페셔널 Instagram 계정, 역할·권한·토큰을 준비합니다.</li><li>토큰은 API 권한을 담는 비밀 문자열이며 비밀번호처럼 보호합니다. 개발자 가입의 현행 인증 화면은 확인 필요입니다.</li><li>지금은 <a href="02-setup.html"><strong>실습 2</strong></a>로 이동합니다. 개발자 앱 생성은 <a href="08-api.html#app">실습 8</a>에서 합니다.</li></ol>',
'오늘의 기본 경로와 선택 API 경로의 준비물 목록을 구분했습니다.',
['개발자 계정이 없어도 실습 2~7을 할 수 있습니다.','인증·개발자 등록에 결제 요구가 보이면 이 실습의 필수 조건이라고 단정하지 말고 공식 안내를 확인하세요.'])
], '<div class="practice-box"><h2>계정은 몇 개까지?</h2><p>앱에서 전환 가능한 계정 수의 현행 상한과 계정별 이메일/전화 인증 세부 조건은 <strong>7r 근거 미확보 — 확인 필요</strong>입니다. 숫자를 확정하지 않습니다. 계정마다 본인이 접근할 인증 수단을 확인하세요. 짧은 시간의 대량 생성은 추가 인증·스팸 판단 위험을 고려해 피하고, 사칭·정지 회피 목적으로 만들지 마세요. 이 위험·약관 세부 적용도 후속 확인 항목입니다.</p></div><div class="practice-box"><h2>프로페셔널 계정은 공개</h2><p>비공개 연습장처럼 취급하지 마세요. 7r은 앱 전환·공개 조건의 본문을 확보하지 못했으므로 <strong>전환 시 공개 안내와 실제 공개 상태를 본인이 확인</strong>해야 합니다(PRAC-20). 테스트 게시물도 공개될 수 있습니다. 검증 뒤 보관/삭제하려면 아래 후보를 확인하세요.</p>'+menu('테스트 게시물을 연 뒤 <strong>더보기 → 보관 / Archive</strong> 또는 <strong>삭제 / Delete</strong>에 해당하는 항목. 지원 포맷·확인창·복원 조건은 미확인입니다. 공개된 복사본까지 지워진다고 가정하지 마세요.', 'S180','테스트 게시물 보관·삭제')+'</div><div class="practice-box"><h2>비밀번호·토큰을 남에게 주지 않기</h2><p>대행·강의·AI 도구에 비밀번호·인증 코드·토큰을 넘기지 마세요. 토큰은 본인 컴퓨터의 비공개 <code>starter-kit/.env</code> 또는 환경변수에만 둡니다. 환경변수는 프로그램에 설정을 전달하는 실행 환경의 값입니다. 공개 저장소·웹 호스팅에는 미디어만 올립니다.</p></div>'),
page('02-setup','키트 설치와 첫 실행','키트 폴더에서 오프라인 첫 결과물을 만든다.', 'PC, 설치할 때의 인터넷, 다운로드한 ZIP', '35분', 'PRAC-25', [], [
step('terminal','터미널에서 폴더 찾기','키트 폴더를 열고 명령 입력을 연습합니다.','명령을 엉뚱한 폴더에서 실행하는 실수를 줄입니다.',
'<ol><li><a href="https://github.com/yonghun-37/guidebooks"><strong>저장소</strong></a>에서 <strong>Code → Download ZIP</strong>을 눌러 내려받고 <strong>압축 풀기</strong>를 합니다. Git은 필요 없습니다.</li><li>터미널은 글자로 명령을 입력하는 창이고, 명령어는 컴퓨터에 시킬 한 줄 작업입니다. Windows는 시작에서 <strong>PowerShell</strong>, macOS는 Spotlight에서 <strong>터미널</strong>을 엽니다.</li><li>폴더 경로는 파일이 있는 위치입니다. 아래 <code>내이름</code>과 Downloads 위치를 실제 경로로 바꾸세요. <code>cd</code>는 폴더 이동입니다. 목록에 <code>run_pipeline.py</code>가 보이면 맞습니다.</li><li>명령은 한 줄씩 붙여 넣고 Enter를 누릅니다. Windows는 Ctrl+V, macOS는 ⌘+V로 붙여 넣습니다. <strong>Ctrl+C</strong>는 실행 중인 명령을 멈춥니다. 중단 후에는 파일이 일부만 생겼을 수 있으니 새 출력 폴더를 쓰세요.</li></ol>',
'목록에 README.md, requirements.txt, run_pipeline.py가 보이고 현재 위치가 starter-kit입니다.',
['ZIP 안에서 바로 실행하지 말고 압축을 푼 폴더로 이동하세요.','공백이 있는 경로는 큰따옴표로 감싸세요.'],
code('cd "C:\\Users\\내이름\\Downloads\\guidebooks-main\\starter-kit"\ndir'),
code('cd "/Users/내이름/Downloads/guidebooks-main/starter-kit"\nls')),
step('python','Python 확인과 설치','Python 3.11 이상을 준비합니다.','키트의 Python 파일을 실행할 도구가 필요합니다.',
'<ol><li>Python은 이 키트의 프로그램을 실행하는 언어와 실행 도구입니다. 아래 OS 탭의 확인 명령을 실행합니다.</li><li>없거나 3.11보다 낮으면 <a href="https://www.python.org/downloads/"><strong>Python 공식 다운로드</strong></a>에서 설치합니다. Windows 설치 화면에 <strong>Add python.exe to PATH</strong>가 있으면 선택합니다. PATH는 실행 파일을 찾을 위치 목록입니다.</li><li>설치 뒤 터미널을 다시 열어 키트로 이동하고 확인 명령을 다시 실행합니다. Windows에서 다른 버전을 설치했다면 이후 <code>py -3.11</code>을 해당 설치 버전으로 바꿉니다.</li></ol>',
'<code>Python 3.11.x</code> 또는 그보다 높은 버전이 출력됩니다. x는 설치된 세부 버전이라 달라도 됩니다.',
['명령 대신 Microsoft Store가 열리면 설치 경로·실행 별칭을 점검하고 py 명령으로 다시 확인하세요.','명령을 찾지 못하면 설치 여부와 PATH를 확인하고 창을 다시 여세요.'],
code('py -3.11 --version'),code('python3 --version')),
step('install','가상환경과 라이브러리 설치','키트 전용 실행 환경에 필요한 패키지를 설치합니다.','다른 프로젝트의 Python 설정과 섞이지 않게 합니다.',
'<ol><li>가상환경 <code>.venv</code>는 이 폴더용 Python과 패키지를 모으는 상자입니다. pip는 패키지 설치 도구입니다.</li><li>아래 OS 명령을 한 줄씩 실행합니다. Windows는 활성화 정책을 바꾸지 않고 <code>.venv\\Scripts\\python.exe</code>를 직접 사용합니다. <strong>이후 모든 python 명령도 이 경로로 바꿉니다.</strong></li><li>macOS는 활성화 뒤 <code>python</code>을 사용합니다. 새 창에서는 다시 폴더 이동·활성화하세요. FFmpeg는 영상 도구이며 키트가 설치 패키지의 바이너리를 사용할 수 있어 별도 설치가 기본 필수는 아닙니다.</li></ol>',
'설치 명령이 오류 없이 끝나고 전용 Python의 버전이 3.11 이상입니다. 설치 로그의 세부 버전·줄 수는 달라도 됩니다.',
['PIL/yaml/imageio_ffmpeg가 없으면 이 가상환경의 Python으로 pip 명령을 다시 실행하세요.','지원 FFmpeg 바이너리가 없는 OS/CPU에서는 README의 오류 표를 확인하세요.'],
code('py -3.11 -m venv .venv\n.venv\\Scripts\\python.exe -m pip install --cache-dir .cache/pip -r requirements.txt\n.venv\\Scripts\\python.exe --version'),
code('python3 -m venv .venv\nsource .venv/bin/activate\npython -m pip install --cache-dir .cache/pip -r requirements.txt\npython --version')),
step('first-run','첫 생성은 합성 자료로','오프라인 샘플을 별도 출력 폴더에 만듭니다.','계정·키 없이 생성부터 검수 대기까지 익힙니다.',
'<ol><li>아래 명령의 <code>output/first-post</code>는 새 결과 폴더입니다. 첫 실행만 이 명령을 사용하고 이후 단계에서는 이어 씁니다.</li><li>완료 후 폴더를 열어 카드와 영상을 확인합니다. 확장자는 파일 이름 끝의 종류 표시로, <code>.png/.jpg</code>는 이미지, <code>.mp4</code>는 영상입니다.</li><li><code>REVIEW.md</code>는 사람이 읽는 검수표입니다. 검수 대기에서 멈추는 것이 정상입니다. 합성 자료는 실제 뉴스가 아니며 live 게시를 거부합니다.</li></ol>',
'<code>검수 대기: …/output/first-post/REVIEW.md</code>가 출력됩니다. 카드 5장의 PNG/JPEG와 reel.mp4가 있고 APPROVED.json은 아직 없습니다.',
['File exists면 기존 결과를 지우지 말고 새 이름으로 바꾸고 이후 모든 경로도 맞추세요.','영상이 무음인 것은 기본 설정입니다. 실습 5에서 녹음을 선택할 수 있습니다.'],
code('.venv\\Scripts\\python.exe run_pipeline.py --offline --output output/first-post'),
code('python run_pipeline.py --offline --output output/first-post'))
], '<p class="note">명령은 로컬 키트 계약(PRAC-25)입니다. 설치만 인터넷이 필요합니다. OS 탭은 명령 차이를 안내하며 Windows/macOS 실기기 성공을 뜻하지 않습니다. 전체 설명은 <a href="https://github.com/yonghun-37/guidebooks/blob/main/starter-kit/README.md">키트 README</a>를 함께 봅니다.</p>'),
page('03-copy','소재 고르기와 웹 채팅 문안','합성 연습 또는 본인 자료의 문안을 검증한다.', '실습 2 출력 폴더, 원자료, 텍스트 편집기, 선택한 웹 채팅', '30분', 'PRAC-25', [], [
step('source','오늘의 소재와 권리 기록','누구의 어떤 질문을 풀지 원자료와 함께 적습니다.','문안 생성 전에 사실과 재사용 가능한 범위를 정합니다.',
'<ol><li>처음에는 동봉 합성 피드로 연습합니다. 실제 게시용은 제목·날짜·URL·핵심 사실·이용 조건을 본인이 확인한 자료로 교체합니다. 실제 뉴스처럼 합성 자료를 게시하지 않습니다.</li><li><a href="../chapters/05-sources.html#workshop"><strong>(이론) 소재·권리 노트</strong></a>에서 허락·인용 범위를 판단합니다. RSS는 업데이트 목록을 전달하는 피드 형식이며 재사용 허락과 별개입니다.</li><li>한 문장 독자 질문과 원출처를 적습니다. 기사 전체·사진을 무단으로 웹 채팅에 복사하지 마세요.</li></ol>'+code('독자 질문:\n원자료 제목 / 날짜 / URL:\n내가 확인한 사실:\n재사용 가능 범위 / 확인이 필요한 것:'),
'독자 질문·원출처·권리 범위가 적힌 소재 메모가 있습니다.',
['원출처가 없으면 생성 전에 찾으세요.','이용 허락이 불분명하면 합성 연습을 유지하거나 권리를 확인한 다른 자료로 바꾸세요.']),
step('prompt','웹 채팅에 붙여 넣을 문서 만들기','기존 news.json에서 prompt.md를 만듭니다.','API 키 없이 사람이 채팅에 전달할 자료를 준비합니다.',
'<ol><li><code>JSON</code>은 필드 이름과 값을 큰따옴표·쉼표로 연결하는 데이터 문서 형식입니다. <code>copy.json</code>에 카드·영상·캡션을 함께 담습니다.</li><li>아래 명령은 웹 채팅을 호출하지 않고 <code>output/first-post/prompt.md</code>만 만듭니다. 기존 copy.json은 보존합니다.</li><li>prompt.md를 본인이 이용 가능한 웹 채팅에 붙여 넣습니다. 수정 작업이면 <strong>현재 copy.json 전체도 함께 제공</strong>하고 원출처·합성 표시를 보존하도록 요청합니다. 웹 서비스 버튼·무료 한도는 이 실습에서 확정하지 않습니다.</li></ol>',
'<code>웹 채팅에 붙여 넣을 프롬프트: …/prompt.md</code>가 출력됩니다. 기존 copy.json이 그대로 있습니다.',
['무료 이용 한도에 걸리면 기존 오프라인 초안을 직접 편집해도 됩니다. 유료 API는 필수가 아닙니다.','채팅에 토큰·비밀번호·민감한 원자료는 넣지 마세요.'],
code('.venv\\Scripts\\python.exe write_copy.py output/first-post/news.json --mode prompt --template cards --output output/first-post/copy.json'),
code('python write_copy.py output/first-post/news.json --mode prompt --template cards --output output/first-post/copy.json')),
step('validate','답변 저장과 구조 검증','전체 JSON을 저장하고 필수 구조를 검사합니다.','화면에 넣을 필드와 원출처 누락을 먼저 잡습니다.',
'<ol><li>답변의 <strong>전체 JSON 객체</strong>만 텍스트 편집기에서 copy.json에 저장합니다. 앞뒤 설명과 <code>```</code> 울타리는 빼세요. 웹 채팅을 쓰지 않았다면 기존 파일을 직접 편집합니다.</li><li>카드의 <code>title</code>과 본문 <code>points</code>, 영상 자막 <code>subtitle</code>, 게시 문구 <code>caption</code>을 확인합니다. 본문 카드는 body 대신 points를 표시하므로 함께 고칩니다.</li><li>아래 검증을 실행하고 인명·날짜·수치·조건을 원문과 직접 대조합니다. 구조 검사는 사실·저작권 검증이 아닙니다. 수정 뒤 실습 4에서 다시 렌더링합니다.</li></ol>',
'<code>구조 검증 OK: output/first-post/copy.json (사실 확인은 사람이 해야 합니다)</code>가 출력됩니다.',
['JSON 오류면 큰따옴표·쉼표·코드 울타리를 확인하세요.','원출처 또는 합성 표시 오류면 필드를 삭제하지 말고 원자료에 맞게 복원하세요.'],
code('.venv\\Scripts\\python.exe write_copy.py output/first-post/news.json --validate --output output/first-post/copy.json'),
code('python write_copy.py output/first-post/news.json --validate --output output/first-post/copy.json'))
], '<p>실습 2의 <code>output/first-post</code>를 계속 사용합니다. 실제 자료로 바꿀 때는 아래 별도 경로를 선택합니다. 이 페이지의 명령은 네트워크를 호출하지 않습니다.</p><details class="practice-box"><summary>실제 자료로 바꾸기: 새 로컬 피드 만들기</summary><p>합성 연습을 한 번 마친 뒤 본인 자료로 게시하려면, 아래 XML의 제목·URL·날짜·요약을 <strong>본인이 확인한 원자료와 자기 문장</strong>으로 모두 바꿔 <code>starter-kit/my-feed.xml</code>에 UTF-8 일반 텍스트로 저장하세요. 예시의 example.org와 안내 문구는 실제 자료가 아닙니다. XML은 시작·끝 태그로 내용을 감싸는 문서 형식입니다. 값에 &amp;를 쓰면 &amp;amp;로 적습니다. 권리·사실이 미확인이면 만들지 말고 보류합니다.</p>'+code('<rss version="2.0"><channel>\n<title>내가 확인한 소재</title>\n<item><title>직접 확인한 제목으로 교체</title>\n<link>https://example.org/replace-with-real-source</link>\n<description>내 말로 다시 쓴 짧은 요약으로 교체</description>\n<pubDate>원자료의 날짜로 교체</pubDate></item>\n</channel></rss>')+code('python run_pipeline.py --offline --feed my-feed.xml --output output/my-news')+'<p>Windows PowerShell에서는 python을 <code>.venv\\Scripts\\python.exe</code>로 바꿉니다. 새 폴더에서 검수 대기로 멈추면 <strong>이후 모든 명령의 output/first-post를 output/my-news로 바꿔</strong> 실습 3~7을 다시 진행합니다. 피드를 바꾸지 않고 synthetic만 false로 고치면 실제 자료가 되지 않습니다. 이 XML에는 합성 태그를 넣지 않으므로 실제 확인한 자료일 때만 사용합니다. news.json·copy.json의 원출처와 문장을 직접 확인합니다.</p></details>'),
page('04-cards','뉴스카드 캐러셀 만들기','순서와 글자를 확인한 카드 파일을 만든다.', '검증한 copy.json, 권리를 확인한 이미지·폰트', '20분', 'PRAC-08 PRAC-10 PRAC-25 API-06', ['S004','S068'], [
step('render','카드 다시 만들기','검증한 문안을 이미지에 반영합니다.','JSON을 고쳐도 이미지가 자동으로 바뀌지 않기 때문입니다.',
'<ol><li>렌더링은 문안·설정을 실제 이미지와 영상 파일로 만드는 작업입니다. 아래 명령은 카드와 릴스를 함께 다시 만듭니다.</li><li><code>cards/card-01.png</code>부터 표지 → 본문 → 마무리 순서로 엽니다. PNG와 같은 내용의 JPEG(.jpg)도 있습니다.</li><li>문안은 copy.json, 현재 출력물의 색·음성 설정은 <code>output/first-post/config.json</code>을 수정합니다. config.yaml 변경은 새 실행부터 반영됩니다.</li></ol>',
'<code>검수 대기: …/output/first-post/REVIEW.md</code>가 출력됩니다. cards/에 card-01부터 card-05까지 PNG와 JPEG가 있습니다.',
['변경이 안 보이면 현재 폴더의 copy.json·config.json을 수정했는지 확인하세요.','렌더링은 기존 승인을 지웁니다. 실패 후에도 새 검수 없이는 게시할 수 없습니다.'],
code('.venv\\Scripts\\python.exe run_pipeline.py render output/first-post'),code('python run_pipeline.py render output/first-post')),
step('legibility','휴대폰 크기로 모든 장 확인','글자·크롭·출처를 카드마다 확인합니다.','첫 장만 좋아 보이고 나머지가 잘리는 문제를 막습니다.',
'<ol><li>모든 PNG/JPEG를 열어 제목·요점·출처·합성 고지를 확인합니다. 길면 문장의 조건과 원출처를 보존하며 줄이고 다시 render합니다.</li><li>키트 카드 1080×1350은 제작 선택입니다. <strong>API 이미지는 JPEG</strong>이며 최대 8MB, 비율 4:5~1.91:1, 너비 320~1440px라는 별도 규격을 따릅니다(API-06). PNG를 API 입력으로 그대로 쓰지 않습니다.</li><li>이 실습은 카드 5장입니다. API 혼합 캐러셀 최대 20개 근거와 앱 선택 화면의 미확인은 구분합니다(PRAC-10). 오늘은 이미지 카드 묶음부터 완성하세요.</li></ol>',
'작은 화면에서도 다섯 카드의 글자·출처가 읽히고 순서가 맞습니다. 실제 앱 선택은 실습 7에서 확인합니다.',
['제목이 잘리면 글을 줄여 재생성하고 전체를 다시 확인하세요.','앱 미리보기 크롭이 달라지면 실습 7에서 각 장을 점검하고 게시를 보류해 수정하세요.'])
]),
page('05-reel','본인 녹음과 릴스 만들기','재생과 자막·음성을 확인한 MP4를 만든다.', '완성 카드, 대본, 선택적으로 본인 녹음 mp3/wav', '25분', 'PRAC-09 PRAC-10 PRAC-25 API-07', ['S004'], [
step('voice','본인 내레이션 준비','본인 대본을 읽어 녹음하거나 무음 연습을 선택합니다.','목소리·음원 권리를 직접 확인할 수 있게 합니다.',
'<ol><li>기본은 무음+자막입니다. 녹음을 원하면 copy.json의 subtitle을 본인 말로 읽고 mp3 또는 wav로 저장합니다. 휴대폰 녹음 앱의 구체적인 버튼은 이 조사에서 확인하지 않았습니다.</li><li>현재 출력 폴더의 <strong>config.json</strong>에서 reel.narration을 본인 파일의 전체 경로로 고칩니다. 아래는 <strong>reel 객체 안에 넣을 필드 예시</strong>이며 config.json 전체를 이것으로 덮어쓰지 않습니다. Windows JSON 경로는 / 또는 이중 역슬래시를 씁니다.</li><li>music은 권리를 확인한 사용자 파일만 선택합니다. tts는 silent를 유지해도 본인 narration 파일을 사용할 수 있습니다. 남의 목소리·음악·글이 섞이면 그 권리는 별도입니다.</li></ol>'+code('"narration": "C:/Users/내이름/Downloads/my-voice.wav",\n"music": null,\n"tts": "silent"'),
'무음 연습을 유지했거나, 실제 존재하는 본인 녹음 경로가 현재 config.json에 지정됐습니다.',
['녹음 파일이 없으면 narration을 null로 두고 무음 연습을 먼저 마치세요.','narration 파일을 바꾸면 다시 render·검수해야 합니다.'],
'녹음 파일 경로 예: <code>C:/Users/내이름/Downloads/my-voice.wav</code>. 확장자를 .wav로 이름만 바꾸는 것은 변환이 아닙니다.',
'녹음 파일 경로 예: <code>/Users/내이름/Downloads/my-voice.wav</code>. config.json 문자열 안에는 큰따옴표를 유지합니다.'),
step('video','릴스 재생성과 끝까지 보기','영상 파일을 다시 만들고 재생합니다.','음성·자막·장면이 실제로 맞는지 파일에서 확인합니다.',
'<ol><li>아래 render 명령을 실행하고 <code>reel.mp4</code>를 처음부터 끝까지 재생합니다.</li><li>기본 샘플은 1080×1920, 20초, 무음+자막입니다. 본인 녹음을 선택했다면 실제 목소리가 들리는지 확인합니다. 자막 시간 자동 음성 정렬은 지원하지 않습니다.</li><li>20초는 학습 예제 길이입니다. API는 MOV/MP4·H.264/HEVC·23~60fps·3초~15분·최대 300MB, 9:16 권장이라는 별도 문서 범위입니다(API-07). 앱 촬영 상한으로 옮겨 쓰지 않습니다.</li><li>릴스와 혼합 캐러셀의 동영상 자식은 다릅니다. 키트는 JPEG 캐러셀과 독립 릴스를 만듭니다.</li></ol>',
'<code>검수 대기: …/output/first-post/REVIEW.md</code>가 출력되고 reel.mp4가 재생됩니다. 기본 샘플은 20초·자막·무음이며 선택 녹음은 실제로 들립니다.',
['기본 무음은 실패가 아닙니다. 녹음 선택 시에도 무음이면 현재 config.json의 narration 경로를 확인하세요.','소리·자막 타이밍이 어긋나면 녹음을 대본 장면 길이에 맞춰 다시 편집하세요.','영상이 열리지 않으면 README의 FFmpeg·플레이어 오류 표를 확인하세요.'],
code('.venv\\Scripts\\python.exe run_pipeline.py render output/first-post'),code('python run_pipeline.py render output/first-post'))
], '<p class="note">정적 카드에 움직임·음성을 더한 사실만으로 추천·수익화 적격을 보장하지 않습니다. 실제 게시의 권리·표시는 <a href="06-review.html">실습 6</a>과 <a href="../chapters/12-safety.html">이론 12장</a>에서 판단합니다.</p>'),
page('06-review','게시 전 사람 검수','사실·권리·표시와 결과물을 확인하고 승인한다.', '원자료, 카드·영상, REVIEW.md, 이론 12장 체크리스트', '20분', 'PRAC-11 PRAC-12 PRAC-22 PRAC-25', ['S071','S008','S183','S184'], [
step('review','여섯 항목 직접 검수','원문·카드·영상·권리·표시를 사람이 확인합니다.','구조 검사와 생성 성공만으로 게시 준비가 끝나지 않습니다.',
'<ol><li><a href="../chapters/12-safety.html#workshop"><strong>이론 12장 게시 전 체크리스트</strong></a>와 출력 폴더 REVIEW.md를 엽니다.</li><li>원출처·날짜·인명·수치·조건을 카드와 대조하고 모든 JPEG와 영상을 봅니다. 내레이션·음원·폰트·사진 권리, 캡션, is_ai_generated를 확인합니다.</li><li>검토한 여섯 줄의 <code>- [ ]</code>를 <code>- [x]</code>로 바꿔 저장합니다. 합성 자료는 연습용임을 확인하는 것이며 실제 뉴스 게시 승인이 아닙니다.</li></ol>',
'REVIEW.md의 여섯 항목을 실제로 검토했고 여섯 줄만 [x]로 저장했습니다. 자동으로 체크하는 명령은 사용하지 않습니다.',
['모르는 권리·사실이 남으면 체크하지 말고 보류하세요.','캡션 수정은 REVIEW.md만 고치지 말고 copy.json을 고친 뒤 render부터 다시 합니다.']),
step('labels','AI·협찬 표시 판단','필요한 표시와 게시 가능 여부를 결정합니다.','캡션과 플랫폼 라벨을 서로 대체한다고 오해하지 않게 합니다.',
'<ol><li>실사형 합성 영상·사실적으로 들리는 합성 음성 등은 AI 자기공개 필요성을 검토합니다. AI 글쓰기 보조를 모두 같은 조건으로 판정하지 않습니다.</li><li>경제적 이해관계가 있으면 국내 표시 기준의 문구와 플랫폼 유료 파트너십 라벨을 각각 확인합니다. 광고 집행 허락은 별개입니다.</li><li>필요한 앱 라벨을 확인하지 못한 콘텐츠는 게시 준비 단계에 남깁니다. 아래 앱 메뉴의 위치는 7v 확인 전 후보입니다.</li></ol>'+
menu('<strong>AI 라벨 추가 / Add AI label · AI 정보 / AI info</strong>. 최종 설정의 <strong>더 많은 옵션 / More options · 고급 설정 / Advanced settings</strong> 안에 있는지도 미확인입니다.', 'S183','게시 전 AI 토글')+
menu('<strong>파트너십 레이블 및 광고 / Partnership label & ads · 유료 파트너십 레이블 추가 / Add paid partnership label</strong>. 계정 자격·파트너 선택·승인 순서는 미확인입니다.', 'S184','게시 전 유료 파트너십·승인'),
'표시 필요 여부·근거·보류할 조건을 적었습니다. 필요한 라벨을 확인할 수 없는 상태는 완료로 판단하지 않습니다.',
['토글이 안 보인다고 의무가 없다고 판단하지 마세요.','캡션에 AI/광고 문구만 넣으면 플랫폼 라벨이 대체된다는 근거는 없습니다.']),
step('approve','승인과 드라이런 확인','검수 기록을 승인하고 요청 미리보기를 봅니다.','실제 전송 전에 파일 변경과 요청 경로를 확인합니다.',
'<ol><li>드라이런은 실제 요청을 보내지 않고 보낼 내용을 출력하는 연습입니다. 아래 approve 명령은 항상 드라이런입니다.</li><li>APPROVED.json은 승인 시 파일 해시를 저장합니다. 해시는 파일이 바뀌었는지 비교하는 요약값입니다. dry-run.json에는 요청 미리보기가 생깁니다.</li><li>캐러셀 자식 JPEG → 상태 확인 → 부모 게시, 릴스 생성 → 상태 확인 → 게시 순서를 읽습니다. 이미지와 영상 URL은 아직 예시입니다. 앱 게시에는 공개 URL이 필요 없습니다.</li></ol>',
'<code>"mode": "dry-run"</code>, <code>"컨테이너 생성"</code>, <code>"상태 확인"</code>, <code>"게시"</code>가 출력되고 APPROVED.json·dry-run.json이 생깁니다. 실제 게시하지 않습니다.',
['여섯 칸 오류면 검수표를 실제로 읽고 저장했는지 확인하세요.','검수 대상 변경 오류면 render → 새 검수 → approve 순서로 다시 합니다.'],
code('.venv\\Scripts\\python.exe run_pipeline.py approve output/first-post\n.venv\\Scripts\\python.exe publish.py output/first-post'),
code('python run_pipeline.py approve output/first-post\npython publish.py output/first-post'))
]),
page('07-publish','앱으로 첫 게시하기','본인 파일을 앱에 게시하고 게시물 주소를 기록한다.', '본인 계정, 실습 6에서 검수한 실제 자료, 휴대폰, 전송 수단', '30분', 'PRAC-17 PRAC-18 PRAC-19 PRAC-21 PRAC-22', ['S192','S193','S194','S068','S066','S183','S184'], [
step('transfer','PC 파일을 휴대폰에 원본으로 저장','검수한 카드와 MP4를 휴대폰에 옮깁니다.','앱에서 원본 파일을 선택할 수 있어야 하기 때문입니다.',
'<ol><li><strong>cards/card-01.jpg~card-05.jpg</strong>와 <strong>reel.mp4</strong>를 준비합니다. 파일 순서·크기·재생을 전송 전후 비교합니다. 앱 게시용 파일을 인터넷 전체에 공개할 필요는 없습니다.</li><li><strong>Windows→Android USB</strong>: 잠금 해제 → 데이터 전송 케이블 연결 → 휴대폰 <strong>USB로 이 기기 충전 중 / Charging this device via USB</strong> 알림 → <strong>USB 사용 / Use USB for → 파일 전송 / File Transfer</strong> → PC에서 복사 → 꺼내기. 일부 단계는 Android 14 이상 문서 기준입니다.</li><li><strong>Drive→iPhone</strong>: PC에서 본인 Drive에 올린 파일을 휴대폰 Drive에서 찾아 <strong>더보기 / More → 사본 보내기 / Send a copy → 이미지 저장 / Save image 또는 동영상 저장 / Save video</strong>로 저장합니다. <strong>Open in → Save to Files</strong>는 사진 보관함 저장과 다릅니다.</li><li><strong>Mac→iPhone</strong>: Wi-Fi·Bluetooth·수신 허용 확인 → 파일의 <strong>공유 / Share → AirDrop</strong> → 본인 기기 → 필요하면 <strong>수락 / Accept</strong>. Finder AirDrop에 끌어놓기도 가능합니다. 사진/파일 앱 중 실제 저장 위치를 확인합니다.</li></ol><p>메신저 전송은 압축 여부가 이번 조사에서 미확인입니다. 카카오톡 등으로 보냈다는 이유만으로 원본이라고 가정하지 말고 위 전송 경로와 전후 비교를 사용하세요.</p>',
'휴대폰에서 카드의 작은 글자까지 읽히고 영상이 끝까지 재생됩니다. PC와 순서·해상도·화질을 비교했습니다.',
['충전만 되면 데이터 케이블과 파일 전송 모드를 확인하세요.','Drive에서 파일 앱에만 보이면 사진 보관함 저장 경로를 다시 확인하세요.','AirDrop에 안 보이면 Wi-Fi·Bluetooth·수신 대상을 확인하고 최신 공식 코드 안내가 나오면 따르세요.'],
'Windows→Android는 USB, Windows→iPhone은 위 Drive 저장 경로를 선택할 수 있습니다. 기기 제조사·앱 UI는 다를 수 있습니다.',
'Mac→iPhone은 AirDrop을 먼저 확인합니다. 다른 조합은 본인 Drive로 파일을 옮긴 뒤 해당 기기의 원본 저장 기능을 확인하세요.'),
step('carousel','카드 묶음 선택과 미리보기','의도한 계정에서 캐러셀 카드 순서를 확인합니다.','다른 계정·뒤섞인 순서·잘린 카드로 게시하지 않게 합니다.',
'<ol><li>앱 프로필의 사용자 이름이 대상 계정인지 확인합니다. 연습 샘플은 실제 뉴스가 아니며, 오늘 공개할 실제 자료는 실습 6 검수를 먼저 마칩니다.</li><li>아래 탐색 후보로 게시물 만들기 화면을 찾아 <strong>여러 항목 선택</strong>에 해당하는 도구로 card-01부터 차례로 선택합니다.</li><li>다음/미리보기에 해당하는 화면에서 모든 장을 넘기며 크롭·출처·순서를 확인합니다. 이 실습은 이미지 5장입니다. 앱 혼합·길이 상한을 단정하지 않습니다.</li></ol>'+
menu('<strong>만들기 / Create(+) → 게시물 / Post → 여러 항목 선택 / Select multiple → 다음 / Next</strong>. 진입 위치·재정렬·권한 화면·Next 횟수는 미확인입니다.', 'S068','캐러셀 진입·사진 선택·순서·크롭'),
'게시 전 미리보기에서 의도한 계정과 카드 5장의 순서·크롭을 본인이 확인했습니다. 아직 공유하지 않습니다.',
['파일이 안 보이면 사진 접근 권한과 저장 위치를 앱 도움말로 확인하세요.','화면이 다르면 아래 공식 도움말의 기능명을 검색하고 추정한 버튼을 반복 누르지 마세요.']),
step('reel','릴스 파일 선택과 미리보기','독립 릴스로 MP4를 가져와 봅니다.','파일 재생과 앱에서 보이는 자막·소리가 같은지 확인합니다.',
'<ol><li>카드 대신 릴스를 먼저 게시해도 됩니다. 두 포맷을 함께 게시하는 것은 필수가 아닙니다.</li><li>아래 후보로 릴스 만들기를 찾아 <strong>reel.mp4</strong>를 가져옵니다. 미리보기에서 시작·끝·표지·자막·소리를 확인합니다.</li><li>원래 녹음이 필요한 영상에 라이선스 미확인 음원을 덧붙여 해결하지 않습니다. 편집 뒤 내용이 바뀌었다면 파일·표시 검수를 다시 합니다.</li></ol>'+
menu('<strong>만들기 / Create(+) → 릴스 / Reel → 갤러리·가져오기 → 편집·미리보기 → 다음 / Next</strong>. 실제 버튼·순서·표지/그리드 편집 배치는 미확인입니다.', 'S066','릴스 가져오기·표지·자막·음성'),
'앱 미리보기에서 선택한 MP4의 내용·자막·음성·표지를 본인이 확인했습니다. 카드만 먼저 게시한다면 이 단계는 나중에 해도 됩니다.',
['음량이 다르면 원본과 앱 음원/음량 설정을 함께 확인하세요.','앱 길이 제한이 보이면 화면의 조건을 읽고 기록하세요. 조사에 상충이 있어 현재 최대값을 단정하지 않습니다.']),
step('caption-label','캡션과 AI·협찬 표시 확인','출처와 필요한 표시를 게시 전에 확인합니다.','게시 뒤 수정이 가능하다고 가정하지 않기 위해서입니다.',
'<ol><li>copy.json의 caption을 붙여 넣고 원출처·줄바꿈·경제적 이해관계 문구를 읽습니다. 표시 판단은 <a href="06-review.html#labels"><strong>실습 6</strong></a>을 따릅니다.</li><li>AI 자기공개·유료 파트너십이 필요한 콘텐츠라면 아래 후보와 공식 도움말에서 해당 기능을 확인합니다. 브랜드 승인·계정 자격은 미확인입니다.</li><li>필요한 라벨을 설정할 수 없으면 공유를 보류합니다. 캡션 설명만으로 라벨 의무를 대체했다고 판단하지 않습니다.</li></ol>'+
menu('<strong>AI 라벨 추가 / Add AI label · AI 정보 / AI info</strong>. <strong>더 많은 옵션 / More options · 고급 설정 / Advanced settings</strong> 안인지, 토글 적용 확인은 미확인입니다.', 'S183','AI 표시 위치·적용')+
menu('<strong>파트너십 레이블 및 광고 / Partnership label & ads → 유료 파트너십 레이블 추가 / Add paid partnership label</strong>. 파트너 선택·승인·광고 집행 허락은 각각 확인해야 합니다.', 'S184','협찬 라벨·파트너 선택·승인'),
'본인이 캡션·출처·필요한 라벨을 확인했고, 확인하지 못한 필수 표시가 없습니다.',
['필수 토글이 없으면 OS·앱 버전·계정 유형을 기록해 공식 도움말로 확인하고 게시를 보류하세요.','광고 허락 버튼과 파트너십 표시를 같은 동작으로 판단하지 마세요.']),
step('share','공유 후 실제 게시물 확인','본인이 공유를 실행하고 결과를 확인합니다.','업로드 시작과 게시 완료를 구분합니다.',
'<ol><li>대상 계정·파일·캡션·표시를 마지막으로 확인한 뒤 본인이 최종 공유를 선택합니다. 작업자는 로그인·공유를 대신하지 않습니다.</li><li>업로드 중 중복해서 누르지 않습니다. 프로필에서 해당 게시물을 열고 카드 마지막 장 또는 릴스 끝까지 확인합니다.</li><li>사용자 이름·내용·순서·음성·표시·공개 상태를 확인합니다. 완료 메시지만으로 성공을 판단하지 말고 게시물 자체를 봅니다.</li><li>게시물 주소를 복사할 수 있는 항목을 찾아 다음 기록 칸에 붙여 넣습니다. 게시 후 수정 메뉴의 라벨 지원도 미확인이므로 사전 확인을 우선합니다.</li></ol>'+
menu('<strong>공유 / Share</strong>에 해당하는 최종 동작 → 프로필의 해당 게시물 → <strong>링크 복사 / Copy link · 공유 / Share</strong> 후보. 버튼 위치·완료 문구·링크 복사 순서는 미확인입니다.', 'S068','최종 공유·게시 확인·게시물 주소 복사')+
menu('게시 후 <strong>더보기 → 수정 / Edit</strong>에 AI·협찬 라벨이 있는지 확인 필요입니다. 보관/삭제도 <a href="01-account.html#test-account">실습 1</a>에서 미확인 후보로 안내합니다.', 'S183','게시 후 수정·AI/협찬 라벨'),
'본인이 실제 게시물을 열어 내용과 표시를 확인하고 게시물 주소를 기록했습니다. 이 교재나 체크 표시가 실게시 성공을 자동 검증하지는 않습니다.',
['멈춘 것 같아도 재공유 전 프로필에서 이미 올라갔는지 확인하세요.','필수 표시가 빠졌다면 공개를 그대로 두지 말고 공식 도움말로 수정/보관/삭제 가능 여부를 확인하세요.'])
], '<p class="note warning">핵심 경로입니다. 공개 URL·개발자 앱·토큰은 필요 없습니다. 아래 Instagram 메뉴는 <strong>7r에서 현행 한국 화면 미확인</strong>인 탐색 후보입니다. 실제 버튼과 다를 수 있으며 성공 화면을 본 것으로 서술하지 않습니다. 파일 전송은 공식 본문 근거지만 실기기 전송은 미검증입니다.</p>'),
page('08-api','선택 · API 자동 게시','권한·토큰·공개 파일과 요청 경로를 구분한다.', '본인 공개 프로페셔널 계정, Meta 개발자 앱·역할, 실제 자료 승인 폴더', '60분 이상 · 선택 심화', 'PRAC-01 PRAC-02 PRAC-03 PRAC-04 PRAC-05 PRAC-06 PRAC-07 PRAC-08 PRAC-09 PRAC-11 PRAC-12 PRAC-13 PRAC-14 PRAC-15 API-01', ['S174','S175','S176','S177','S179','S178','S031','S030','S001','S004','S185','S186','S187','S188'], [
step('app','개발자 앱과 역할 준비','문서의 Instagram Login 앱 생성 흐름을 확인합니다.','앱 로그인·권한·계정 유형이 맞아야 요청할 수 있습니다.',
'<ol><li><a href="https://developers.facebook.com/apps"><strong>Meta App Dashboard</strong></a>에서 본인 개발자 등록·인증 안내를 확인합니다. 등록 마법사의 현행 화면은 미확인입니다.</li><li>문서 기준은 <strong>Create App → Other → Next → Business → Next → 앱 이름·연락 이메일 → Next → Instagram → Set up</strong>입니다. 다른 use case 마법사가 보이면 그대로 강요하지 말고 Instagram 제품과 API setup 항목을 확인합니다.</li><li><strong>Instagram → API setup with Instagram login</strong>의 토큰 영역에 본인 공개 계정을 추가합니다. 계정·역할은 <strong>App Roles → Roles</strong> 또는 API setup에서 확인합니다. Administrator/Developer/Tester 중 본인 역할을 확인합니다.</li><li>본인 소유·관리 계정 Standard Access와 외부 고객용 Advanced Access·앱 검수를 구분합니다. 개발 모드의 역할 사용자 테스트와 일반 공개는 별개입니다. 공통 App Modes는 비역할 사용자 비노출을 설명하고 생성 문서의 live data 검수 안내와 범위 차이가 있습니다. <strong>검수 면제만으로 일반 독자 공개를 보장하지 않습니다.</strong></li></ol>'+
menu('<strong>Instagram 테스터 초대 수락</strong> 항목의 현행 경로 확인 필요. Facebook Authorized App Tester의 수락 경로를 Instagram 앱 메뉴로 옮기지 않습니다.', 'S179','Instagram 테스터 초대 수락'),
'문서와 본인 대시보드에서 Instagram Login 제품·대상 계정·역할·권한을 구분했습니다. 실제 계정 API 게시 성공은 아직 확인 전입니다.',
['Instagram 제품이 없으면 앱 유형/use case를 공식 생성 문서와 비교하세요.','권한 오류를 해결하려고 불필요한 전체 권한이나 Live 전환을 먼저 하지 마세요.']),
step('token','토큰과 로컬 .env 준비','토큰·계정 ID·버전을 비공개 환경에 둡니다.','비밀 값을 공개 코드나 명령 기록에 남기지 않기 위해서입니다.',
'<ol><li>공식 문서의 <strong>Instagram → API setup with Instagram business login → Generate token</strong> 경로를 확인합니다. 다른 생성 문서에는 with Instagram login이라고 적혀 있으므로 실제 화면에서 대상 항목을 확인합니다.</li><li>문서상 Generate token은 <strong>60일 장기</strong>, Business Login OAuth는 <strong>1시간 단기</strong>입니다. 실제 expires_in·권한 취소 상태를 확인합니다.</li><li><code>.env.example</code>을 <code>.env</code>로 복사하고 본인 편집기에서 IG_ACCESS_TOKEN·IG_USER_ID를 입력합니다. 아래 예시는 빈 값이며 실제 토큰을 채팅·스크린샷에 넣지 않습니다. 기본 버전은 <strong>v26.0</strong>(2026-07-29 출시, PRAC-01)입니다. 환경변수가 .env보다 우선합니다.</li><li>대상 ID·사용자 이름 확인은 공식 문서의 <code>GET /v26.0/me?fields=user_id,username</code>를 비공개 실행 환경에서 인증해 확인합니다. 토큰이 다른 계정 것이 아닌지 확인하세요.</li><li>장기 토큰은 발급 <strong>24시간 이후·만료 전</strong>에 <code>GET https://graph.instagram.com/refresh_access_token</code>의 <code>grant_type=ig_refresh_token</code>·access_token으로 다시 <strong>60일</strong> 갱신할 수 있습니다. 비공개 환경에서 공식 문서대로 실행하고 반환된 값·만료 정보를 확인합니다. 만료했다면 재인증합니다. 키트는 자동 갱신하지 않습니다.</li></ol>'+code('IG_ACCESS_TOKEN=\nIG_USER_ID=\nIG_API_VERSION=v26.0'),
'토큰과 숫자 계정 ID가 본인 컴퓨터의 .env 또는 환경변수에만 있고 공개 저장소에는 없습니다. 대상 계정과 만료 시점을 본인이 확인했습니다.',
['토큰 만료면 갱신 요청을 반복하지 말고 재인증하세요.','권한은 instagram_business_basic·instagram_business_content_publish를 확인합니다. *_publishing으로 오기하지 않습니다.'],
code('Copy-Item .env.example .env')+'메모장으로 .env를 열어 편집합니다. 파일 이름이 .env.txt가 되지 않게 확인하세요.',
code('cp .env.example .env')+'텍스트 편집기의 일반 텍스트 모드로 .env를 편집합니다.'),
step('hosting','승인 파일로 공개 URL 만들기','JPEG와 MP4만 별도 공개 폴더로 준비합니다.','Instagram Login은 이미지·동영상 모두 Meta가 읽을 공개 URL이 필요합니다.',
'<ol><li>실습 6 승인을 마친 본인 실제 자료 출력 폴더에 아래 도우미를 실행합니다. 예시는 first-post지만 합성 샘플은 live 게시할 수 없습니다.</li><li>도우미는 승인된 JPEG/MP4만 새 폴더에 복사합니다. .env·검수표·설정·토큰은 복사하지 않습니다. 네트워크 요청은 없습니다.</li><li>본인의 <strong>별도 공개 GitHub 저장소 → Add file → Upload files</strong>에서 hosting/first-post 안의 <strong>cards 폴더와 reel.mp4</strong>를 함께 드래그 앤 드롭하고 <strong>Commit changes</strong>로 저장합니다.</li><li><strong>Settings → Pages → Build and deployment → Source: Deploy from a branch</strong>에서 branch와 <strong>/(root)</strong>를 고르고 배포 완료를 확인합니다. 업로드를 하위 폴더에 했다면 기본 URL에도 그 경로를 포함합니다.</li><li>로그인하지 않은 창에서 <code>https://사용자.github.io/저장소/cards/card-01.jpg</code>와 <code>/reel.mp4</code>가 파일 자체로 열리는지 확인합니다. <code>curl -I -L "실제 파일 URL"</code>로 헤더·최종 URL·MIME도 확인할 수 있지만 실제 GET 파일 열기를 대신하지 않습니다.</li><li>기본 URL은 두 파일 경로의 공통 부모 폴더입니다. localhost·로컬 경로·Drive 미리보기·/blob/ HTML 주소는 대체가 아닙니다. Meta 수신 성공은 별도로 확인해야 합니다.</li></ol><p>GitHub 웹 업로드는 파일당 <strong>25MiB</strong>입니다. Pages는 Free 공개 저장소에서 가능한 작은 교육 실습 후보지만 사업 운영용 무료 호스팅을 제한합니다(PRAC-14·15). 수익화 미디어의 상시 CDN으로 포괄 권장하지 않습니다.</p>',
'기본 카드 5장일 때 <code>공개 준비 완료: 6개 JPEG/MP4 → …</code>가 출력됩니다. 공개 폴더에는 cards/*.jpg와 reel.mp4만 있고 배포 후 로그인 없이 파일 자체가 열립니다.',
['승인 파일 변경 오류면 render·새 검수·approve부터 다시 하세요.','대상 폴더가 이미 있으면 새 이름을 지정하세요. 파일당 25MiB 초과면 크기를 조정해 다시 검수합니다.','공개 창에서 열려도 Meta의 다운로드는 봇 차단·접근 제어로 실패할 수 있습니다.'],
code('.venv\\Scripts\\python.exe prepare_hosting.py output/first-post --dest hosting/first-post'),
code('python prepare_hosting.py output/first-post --dest hosting/first-post')),
step('request','요청 미리보기와 선택 live 실행','실제 URL의 드라이런을 확인하고 본인이 게시 여부를 결정합니다.','컨테이너 생성과 게시를 구분하고 중복 재시도를 피합니다.',
'<ol><li>아래 <code>&lt;URL&gt;</code>을 cards/와 reel.mp4가 있는 본인 HTTPS 폴더 주소로 바꿉니다. 먼저 <strong>--live 없는 명령</strong>으로 JPEG image_url·MP4 video_url 경로를 봅니다.</li><li>공식 흐름은 자식 컨테이너 생성 → status_code=FINISHED → 부모 생성·상태 확인 → media_publish입니다. 릴스도 생성·상태 확인·발행을 따릅니다. 키트는 FINISHED가 될 때까지 분당 1회 간격으로 최대 5회 확인하고 실패를 남깁니다. 미발행 컨테이너는 24시간 후 만료합니다.</li><li>live는 <strong>캐러셀과 릴스 2개 게시 시도</strong>입니다. 실제 자료·표시·권한·공개 URL·토큰을 모두 확인했을 때만 README의 live 명령을 본인이 선택합니다. 키트는 AI 자기공개를 부모/독립 릴스에만 설정하고 Instagram Login의 협찬 API 파라미터는 지원하지 않습니다.</li><li>API 게시 한도 문서의 100/50 상충은 단일값으로 정하지 않습니다. content_publishing_limit의 실효값을 확인합니다. Instagram Login용 재개 업로드 근거는 없으므로 JPEG/MP4 공개 URL을 생략하지 않습니다.</li></ol>'+code('python publish.py output/first-post --live --base-url "<URL>"')+'<p class="note warning">바로 위는 실제 2개 게시를 시도하는 선택 명령입니다. 이 작업에서는 실행하지 않았습니다. Windows에서는 python을 전용 실행 파일 경로로 바꾸세요. 합성 샘플은 거부됩니다.</p>',
'드라이런은 <code>"mode": "dry-run"</code>과 본인 URL을 표시합니다. live를 본인이 선택했다면 LIVE_ATTEMPT.json의 상태·미디어 ID와 앱 게시물·공개 범위를 직접 확인해야 완료입니다. 문서만으로 live 성공을 보장하지 않습니다.',
['권한 오류면 계정·역할·scope·토큰 대상부터 확인하세요.','ERROR/EXPIRED/시간 초과는 성공이 아닙니다. 기록과 대시보드를 확인하세요.','응답이 끊겼으면 일부 게시가 이미 됐을 수 있습니다. LIVE_ATTEMPT.json을 지우고 재실행하지 마세요.'],
code('.venv\\Scripts\\python.exe publish.py output/first-post --base-url "<URL>"'),
code('python publish.py output/first-post --base-url "<URL>"'))
], '<p class="note warning">선택 심화입니다. 실습 7을 마치는 데 필요하지 않습니다. 문서상 본인 계정 테스트 조건과 일반 공개는 구분합니다. 개발자 등록·권한·실게시·일반 독자 공개를 작업자가 검증하지 않았습니다. API 호출은 본인이 판단하며 이 교재의 검증은 모킹입니다.</p>'),
page('09-schedule','선택 · 예약과 자동 실행','예약 여부·시간대·취소 경로를 확인하고 기록한다.', '검수한 게시물, 예약 기능을 제공하는 본인 계정', '20분 · 선택 심화', 'PRAC-23 PRAC-07 PRAC-13', ['S037','S038','S040','S004','S030'], [
step('schedule','예약 가능한 화면 찾기','필요한 표시를 유지하며 예약할 수 있는지 확인합니다.','예약 기능이 보인다는 이유만으로 모든 콘텐츠를 처리한다고 가정하지 않습니다.',
'<ol><li>최종 게시 설정에서 아래 후보의 예약 기능을 찾아봅니다. 보이지 않으면 수동 앱 게시 경로로 돌아갑니다. 국가 전체의 비지원으로 단정하지 않습니다.</li><li>현지 날짜·시간·시간대·대상 계정·파일·캡션·필요한 AI/협찬 표시를 확인합니다. 30일/75일 자료 상충으로 현행 한국 예약 한도를 확정하지 않습니다.</li><li>Business Suite를 선택한다면 본인 프로필 연결/접속 조건을 먼저 확인합니다. 데스크톱의 정확한 버튼·페이지 연결 조건은 이번 조사에서 미확인입니다.</li></ol>'+
menu('<strong>더 많은 옵션 / More options · 고급 설정 / Advanced settings → 이 게시물 예약 / Schedule this post · 이 릴스 예약 / Schedule this reel → 예약 / Schedule</strong>. 날짜·라벨·음원 조합 지원도 확인 필요입니다.', 'S037','앱 예약 진입·날짜·라벨')+
menu('Business Suite 데스크톱의 <strong>콘텐츠 만들기 → Instagram 대상 → 일정 옵션 → 예약 → Planner/Content</strong>는 탐색 후보입니다. S039 모바일 문서를 데스크톱 순서로 적용하지 않습니다.', 'S040','Business Suite 대상·시간대·예약'),
'본인 화면에서 날짜·시간·대상·필수 표시를 확인했고 예약 완료 상태를 확인했습니다. 안 되면 보류 또는 수동 게시로 기록합니다.',
['필수 라벨·음원 지원이 불명확하면 예약하지 말고 실습 7로 돌아가세요.','저장됐는지 모를 때 새 예약을 반복하지 말고 목록부터 확인하세요.']),
step('scheduled-list','예약 목록과 취소 경로 확인','예약한 항목을 다시 찾아 수정·취소 가능 여부를 확인합니다.','잘못된 시간이나 중복 예약을 발견할 수 있게 합니다.',
'<ol><li>예약 직후 목록에서 대상 계정·예약 시각·파일·캡션을 다시 확인합니다.</li><li>수정·취소가 필요한 경우 아래 후보와 공식 도움말을 확인합니다. 취소했다고 생각한 뒤에는 목록 상태도 다시 봅니다.</li><li>예약 시각 뒤 실제 게시물과 표시를 본인이 확인합니다. 예약 저장은 실제 게시 완료가 아닙니다.</li></ol>'+
menu('<strong>프로필 메뉴 → 예약된 콘텐츠 / Scheduled content</strong> 또는 Business Suite의 <strong>Planner/Content → 수정·취소</strong>. 현행 번역·지원·버튼 순서는 미확인입니다.', 'S037','예약 목록·수정·취소·시각 후 게시'),
'예약 시각·확인한 목록·수정/취소 경로와 실제 게시 여부를 기록했습니다.',
['목록이 안 보이면 예약 도구·대상 계정·날짜 필터를 확인하세요.','예약 시각이 지나도 게시물이 없으면 실패 상태부터 확인하고 중복 업로드를 피하세요.']),
step('automation','자동 실행의 경계 정하기','생성·검수·게시·갱신을 별도 작업으로 구분합니다.','검수와 토큰 만료를 건너뛴 자동화를 만들지 않기 위해서입니다.',
'<ol><li>키트는 예약 서비스·호스팅·토큰 자동 갱신을 제공하지 않습니다. OS 스케줄러 등록은 이번 조사·구현 범위가 아닙니다.</li><li>자동 실행을 계획한다면 <strong>생성 → 사람 검수 대기 → 승인한 자료만 전송</strong>으로 나눕니다. 승인 명령은 드라이런입니다.</li><li>컨테이너는 미발행 상태에서 24시간 후 만료하므로 먼 미래 게시용으로 미리 만들지 않습니다. 토큰은 24시간 이후·만료 전에 갱신할 별도 비공개 절차가 필요합니다.</li></ol>'+code('예약 도구 / 대상 계정:\n현지 게시 시각 / 시간대:\n필수 라벨 확인:\n사람 검수·승인할 시점:\n예약 목록·취소 위치:\n실제 게시 확인 결과:'),
'예약 기록에 검수·시간대·취소·게시 확인이 포함되고, 키트가 제공하지 않는 기능을 구분했습니다.',
['승인 없이 전송하는 자동화를 만들지 마세요.','발행 응답 유실 뒤 전체 파이프라인을 다시 돌리기 전에 기존 게시 상태를 확인하세요.'])
]),
page('10-insights','첫 24시간·7일 지표','같은 게시물의 범위와 지표를 두 시점에 기록한다.', '게시물 주소, 본인 계정, 기록 파일', '15분씩 · 교재 관찰 시점', 'PRAC-24', ['S195','S109','S110','S111'], [
step('find','같은 게시물의 인사이트 열기','게시물 주소와 관찰 범위를 확인합니다.','다른 기간·다른 게시물의 수치를 섞지 않기 위해서입니다.',
'<ol><li>실습 7에서 기록한 게시물 주소와 계정·포맷·게시 시각을 확인합니다.</li><li>아래 후보로 해당 게시물의 인사이트를 찾습니다. 계정 합계와 단일 게시물을 구분하고 날짜 필터·단위를 적습니다.</li><li><strong>첫 24시간·7일</strong>은 교재의 관찰 시점입니다. Instagram이 정한 성공 판정 기한이 아닙니다.</li></ol>'+
menu('<strong>게시물 → 인사이트 보기 / View insights</strong> 또는 <strong>프로필 → 프로페셔널 대시보드 / Professional dashboard → 인사이트 / Insights</strong>. 날짜 필터·메뉴 배치는 미확인입니다.', 'S195','게시물 인사이트·프로 대시보드·기간 필터'),
'관찰한 게시물 주소·계정·기간·포맷과 화면의 단위가 기록됐습니다.',
['화면을 못 찾으면 공식 도움말에서 기능을 확인하고 완료로 표시하지 마세요.','프로페셔널 전환 전 데이터의 앱 보존 범위를 임의로 가정하지 마세요.']),
step('metrics','표시된 값과 미제공을 구분','조회·도달·저장·공유와 시청시간을 그대로 기록합니다.','서로 다른 지표를 같은 사람 수나 성공 점수로 읽지 않습니다.',
'<ol><li>조회는 반복 표시/재생을 포함할 수 있고 도달은 고유 계정 추산입니다. 저장·공유도 모두 고유 사람 수라고 해석하지 않습니다.</li><li>유료/자연, Instagram/Facebook 합산, 계정/게시물, 기간을 함께 적고 화면의 단위를 보존합니다. 릴스 시청시간은 화면이 제공할 때 기록합니다.</li><li>값이 없으면 <strong>미제공</strong>으로 씁니다. 0으로 채우지 않습니다. 평균 시청시간을 조회로 임의 나누어 만들지 않습니다.</li></ol>'+code('게시물 주소 / 계정 / 포맷 / 게시 시각:\n관찰 시각 / 집계 기간 / 범위:\n조회 / 도달 / 저장 / 공유:\n릴스 시청시간 / 화면 단위:\n유료·자연 / IG·FB 합산 여부:\n미제공 항목 / 확인할 조건:'),
'숫자 옆에 범위·기간·단위가 있고 없는 값은 미제공으로 남겼습니다.',
['빈 값은 계정 유형·지원 지표·전환 시점·집계 지연을 확인할 항목으로 남기세요.','조회 0이나 저장 0만으로 제재를 단정하지 마세요.']),
step('next','다음 한 편에서 바꿀 것 하나','두 관찰 시점의 기록으로 다음 수정점을 정합니다.','한 게시물의 숫자를 수익 예측이나 성장 보장으로 바꾸지 않습니다.',
'<ol><li>첫 24시간과 7일에 같은 기록 양식을 씁니다. 비교 가능한 범위인지 먼저 확인합니다.</li><li><a href="../chapters/11-analytics.html"><strong>이론 11장 지표 읽기</strong></a>에서 해석을 확인하고 제목·표지·설명 방식 중 다음에 바꿀 것 하나를 적습니다.</li><li><a href="../chapters/14-plan.html"><strong>이론 14장 계획</strong></a>에 실제 제작·검수 시간을 반영합니다. 고정 성장 기준·수익 예측 수치는 추가하지 않습니다.</li></ol>',
'두 시점의 관찰 기록과 다음 한 편에서 바꿀 점 하나가 있습니다.',
['표본이 작으면 원인을 확정하지 말고 관찰을 더 모으세요.','조회만 높아도 실제 수입·비용과는 별도로 기록하세요.'])
])
]


def tabs(index, item):
    prefix = f'os-{index}-{item["id"]}'
    return f'''<div class="os-tabs" data-os-tabs><div data-tab-list aria-label="운영체제별 안내"><button type="button" id="{prefix}-win-tab" data-os-tab="windows" aria-controls="{prefix}-win">Windows</button><button type="button" id="{prefix}-mac-tab" data-os-tab="macos" aria-controls="{prefix}-mac">macOS</button></div><div id="{prefix}-win" data-os-panel="windows" aria-labelledby="{prefix}-win-tab"><h4>Windows</h4>{item['win']}</div><div id="{prefix}-mac" data-os-panel="macos" aria-labelledby="{prefix}-mac-tab"><h4>macOS</h4>{item['mac']}</div></div>'''


def render_step(index, number, item):
    key=f'{index}:{item["id"]}'
    return f'''<section class="chapter-block practice-step" id="{item['id']}" data-step="{key}"><p class="block-label">STEP {number:02} · {E(item['title'])}</p><h2>{E(item['title'])}</h2>
<div class="practice-now"><h3>지금 하는 일</h3><p>{item['now']}</p></div><div class="practice-why"><h3>왜 하는지</h3><p>{item['why']}</p></div>
<div class="practice-follow"><h3>따라 하기</h3>{item['follow']}</div>
<div class="practice-success"><h3>이렇게 보이면 성공</h3><p>{item['success']}</p></div>
<div class="practice-errors"><h3>이렇게 보이면?</h3><ul>{''.join('<li>'+e+'</li>' for e in item['errors'])}</ul></div>
{tabs(index,item)}<label class="practice-check"><input type="checkbox" data-practice-check="{key}"> 이 단계 확인: {E(item['title'])}</label></section>'''


def shell(slug, title, content, index=None):
    track_attr = f'data-practice="{slug}"'
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{E(title,quote=True)} — 처음 시작하는 인스타그램 실습"><title>(실습) {E(title)} | ReelsBook</title><link rel="icon" href="data:,"><link rel="stylesheet" href="../assets/book.css"><script src="../assets/book.js" defer></script><script src="../assets/practice.js" defer></script></head>
<body {track_attr}><a class="skip-link" href="#main">본문으로 건너뛰기</a><header data-site-header><a href="../index.html">ReelsBook</a></header><div class="book-layout"><aside data-book-sidebar aria-label="책과 실습 내비게이션"></aside><main id="main" class="chapter practice-main">
{content}</main></div><footer data-site-footer></footer></body></html>\n'''


def diagram(page, index):
    labels = ['시작 준비','계정·보안','키트 설치','문안 확인','카드 순서','영상·자막','검수·승인','게시 전 확인','권한·공개 URL','예약 확인','기간·범위']
    rows = [
      ['준비물 확인','기본 경로 0~7','선택 심화 8·9'],
      ['대상 계정 확인','유형·인증 확인','복구 수단 보관'],
      ['키트 폴더 확인','Python·패키지 설치','검수 대기 출력'],
      ['원자료·권리 확인','문안·원출처 대조','JSON 구조 검증'],
      ['카드 순서 확인','작은 글자·출처 보기','전체 장 검수'],
      ['대본·음성 확인','영상 끝까지 재생','자막·소리 점검'],
      ['사실·권리 확인','필요한 표시 결정','승인 후 드라이런'],
      ['대상 계정 확인','카드·영상 미리보기','출처·라벨 점검'],
      ['계정·권한 확인','공개 파일 URL 확인','요청·응답 기록'],
      ['계정·시각 확인','시간대·표시 점검','예약 목록 확인'],
      ['같은 게시물 찾기','기간·단위 기록','미제공 값 구분']
    ][index]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 460" role="img" aria-labelledby="title desc"><title id="title">실습 {index} 설명 도식</title><desc id="desc">실제 앱 화면이 아닙니다. 휴대폰 틀 안의 1 {rows[0]}, 2 {rows[1]}, 3 {rows[2]}을 순서대로 강조합니다. 버튼 위치는 설명용입니다.</desc><rect width="360" height="460" rx="20" fill="#eaf0e5"/><rect x="52" y="20" width="256" height="394" rx="30" fill="#fffefa" stroke="#30624f" stroke-width="3"/><rect x="137" y="30" width="86" height="7" rx="3" fill="#dcded4"/><g font-family="system-ui,sans-serif" fill="#202d29"><text x="72" y="78" font-size="19" font-weight="700">{labels[index]}</text><rect x="72" y="102" width="216" height="53" rx="10" fill="#eaf0e5" stroke="#30624f" stroke-width="2"/><text x="86" y="135" font-size="16">1  {rows[0]}</text><rect x="72" y="180" width="216" height="110" rx="10" fill="#f3e8d6"/><text x="86" y="222" font-size="16">2  {rows[1]}</text><path d="M88 246h168m-168 20h125" stroke="#626d66" stroke-width="3"/><rect x="72" y="320" width="216" height="55" rx="10" fill="#30624f"/><text x="86" y="354" font-size="16" fill="#fffefa">3  {rows[2]}</text><text x="52" y="442" font-size="12">설명용 위치 · 화면이 다를 수 있음 · 2026-10-26</text></g></svg>\n'''



def build():
    (SITE/'practice').mkdir(exist_ok=True)
    (SITE/'assets/img/practice').mkdir(parents=True,exist_ok=True)
    e2e=[]
    for index,p in enumerate(PAGES):
        title=f'{index}. {p["title"]}'
        sources=''.join(f'<li id="source-{sid.lower()}">{official(sid)} · <a href="../credits.html#{sid.lower()}">확인 범위·날짜</a></li>' for sid in p['sources'])
        heading=f'''<header class="chapter-hero"><p class="kicker" data-chapter-kicker>(실습) 실습편 / {index}</p><h1 data-chapter-title>(실습) {title}</h1><p class="lead">{p['goal']}</p><dl class="practice-meta"><div><dt>준비물</dt><dd>{p['supplies']}</dd></div><div><dt>시간 배분 예시</dt><dd>{p['minutes']} · 실측 아님</dd></div><div><dt>선행 실습</dt><dd>{f'<a href="{PAGES[index-1]["slug"]}.html">실습 {index-1}</a>' if index else '없음'}</dd></div></dl><p class="small">2026년 10월 조사 기준 · 확인일 2026-10-26 · 근거: {p['facts']} · <a href="e2e.html">E2E 한눈에 보기</a></p><p class="practice-storage" data-practice-status role="status">진행 기록은 자바스크립트를 켜면 이 브라우저에 저장합니다.</p><details data-mobile-outline><summary>이 실습의 흐름</summary></details></header>'''
        fig=f'''<figure class="practice-figure"><img src="../assets/img/practice/{p['slug']}.svg" alt="실습 {index} 설명용 휴대폰 도식: 1 대상 확인, 2 내용 미리보기, 3 완료 전 점검. 실제 UI와 버튼 위치는 다를 수 있습니다."><figcaption>직접 그린 설명 도식 · 실제 앱 스크린샷이 아닙니다. 위치는 설명용이고 화면이 다를 수 있음 · 확인일 2026-10-26. {official(p['sources'][0]) if p['sources'] else '로컬 키트·교재 편집 순서'}</figcaption></figure>'''
        content=heading+p['intro']+fig+''.join(render_step(index,n,item) for n,item in enumerate(p['steps'],1))
        if index==7:
            content+='''<section class="practice-celebrate" id="posted"><p class="eyebrow">오늘의 결과를 기록하세요</p><h2>내가 확인한 첫 게시물, 여기에 남기기</h2><p>실제 게시물을 열어 확인했다면 첫 게시를 마쳤습니다. 수고하셨습니다. 이 기록 칸은 주소를 보관하며 게시 성공을 자동 판정하지 않습니다.</p><label for="posted-url">실제 게시물 주소 붙여 넣기</label><input id="posted-url" type="url" maxlength="500" placeholder="https://www.instagram.com/p/…/" data-practice-field="posted-url"><p class="small">이 브라우저에만 저장합니다. 비밀번호·토큰을 입력하지 마세요. 저장이 차단되면 개인 메모에 주소를 보관하세요.</p><p data-practice-field-status role="status"></p><a href="10-insights.html">실습 10 · 첫 관찰 기록으로 →</a></section>'''
        content+=f'''<section class="chapter-block practice-output" id="output"><h2>지금 내 손에 있는 것</h2><p>{p['goal']} 아래 단계 확인을 모두 마쳤는지 E2E에서 다시 봅니다. 선택하지 않은 포맷·심화는 미완료로 남겨도 됩니다.</p><ul>{''.join(f'<li><a href="#{item["id"]}">{E(item["title"])}</a></li>' for item in p['steps'])}</ul><p><a href="e2e.html">전체 진행 체크리스트 보기 →</a></p></section><aside class="source-notes"><h2>근거와 확인 범위</h2><p data-fact-id="{p['facts']}">{p['facts']}. 앱 메뉴 미확인은 data-verify로 표시했습니다. 로컬 명령은 키트 README·코드 계약(PRAC-25)이며 외부 서비스 성공을 보장하지 않습니다.</p><ul>{sources}</ul></aside><nav data-chapter-pager aria-label="이전·다음 실습">{f'<a href="{PAGES[index+1]["slug"]}.html">다음: 실습 {index+1} →</a>' if index<10 else '<a href="e2e.html">E2E 한눈에 보기 →</a>'}</nav>'''
        (SITE/f'practice/{p["slug"]}.html').write_text(shell(p['slug'],title,content,index))
        (SITE/f'assets/img/practice/{p["slug"]}.svg').write_text(diagram(p,index))
        e2e.append(f'''<section class="chapter-block" id="practice-{index}"><h2><a href="{p['slug']}.html">(실습) {title}</a></h2><p>{'선택 심화 · ' if index in (8,9) else ''}{p['goal']}</p>{''.join(f'<div class="e2e-item"><label><input type="checkbox" data-practice-check="{index}:{item["id"]}">{E(item["title"])}</label><a href="{p["slug"]}.html#{item["id"]}" aria-label="실습 {index} {E(item["title"],quote=True)} 단계로">단계로 →</a></div>' for item in p['steps'])}</section>''')
    (SITE/'practice/e2e.html').write_text(shell('e2e','E2E 한눈에 보기','''<header class="chapter-hero"><p class="kicker">(실습) 전 단계 체크리스트</p><h1>(실습) E2E 한눈에 보기</h1><p class="lead">실습 0~7은 오늘의 기본 경로, 8·9는 선택 심화, 10은 게시 뒤 관찰입니다. 체크는 본인의 기록이며 게시 성공의 자동 판정이 아닙니다.</p><p class="practice-storage" data-practice-status role="status">자바스크립트를 켜면 진행을 이 브라우저에 저장합니다.</p><progress data-practice-progress max="100" value="0" aria-label="전체 실습 단계 진행"></progress><p>각 체크는 해당 실습과 공유됩니다. 저장이 실패해도 현재 페이지에서 계속 체크할 수 있으며 이동 전 개인 메모로 보관하세요. 서버 동기화는 없습니다.</p><button type="button" data-practice-reset>실습 진행·게시물 주소 기록 지우기</button></header>'''+''.join(e2e)+'''<p><a href="00-start.html">실습편 시작으로 →</a></p><noscript><p>체크 기록·OS 탭 전환에는 자바스크립트가 필요합니다. 본문과 양쪽 OS 설명은 그대로 읽을 수 있습니다.</p></noscript>'''))
    # 모든 data-verify 블록에서 현재 문구·화면을 추출한다. 빠뜨린 후보가 없게 원고를 기준으로 만든다.
    rows=[]
    for index,p in enumerate(PAGES):
        text=(SITE/f'practice/{p["slug"]}.html').read_text()
        for m in re.finditer(r'<div class="menu-unverified" data-verify="app-menu" data-screen="([^"]+)">(.*?)</div>',text,re.S):
            sections=list(re.finditer(r'<section[^>]*\bid="([^"]+)"',text[:m.start()]))
            anchor=sections[-1][1] if sections else 'main'
            current=html.unescape(re.sub('<[^>]+>',' ',m[2]))
            current=re.sub(r'\s+',' ',current).strip().replace('|','\\|')
            rows.append(f'| [실습 {index}](../../site/practice/{p["slug"]}.html#{anchor}) | {anchor} | {html.unescape(m[1])} | {current} |')
    (ROOT/'docs/results/phase-7w-verify-list.md').write_text('''# Phase 7w — 7v 앱 메뉴 확인 목록

2026-10-26. 7r에서 본문/실기기 화면을 확보하지 못한 후보를 실제 원고의 `data-verify="app-menu"`에서 추출했다. 사용자 테스트 계정을 제공받는 7v에서만 확인한다. 가입·연락처·+별칭·계정 수 상한·공개 조건·보관/삭제는 근거 공백이 있으며 전환 도움말을 가입/삭제 절차 증거로 쓰지 않는다.

확인 시 OS·앱 버전·언어·계정 유형·확인일·정확한 메뉴와 성공/보류 결과를 기록한다. 라벨·예약·지표는 지원 여부와 실제 적용을 따로 확인한다. 개인정보·QR·토큰·연락처는 남기지 않는다. 확인된 블록만 근거/문구를 갱신하고 미확인 속성을 제거한다. 개발 모드 일반 공개와 테스터 초대 수락도 별도 실증이 필요하다.

| 실습 | 단계 | 확인할 화면 | 현재 문구 |
| --- | --- | --- | --- |
'''+ '\n'.join(rows)+'\n\n추가 공백: 앱 계정 전환 수 상한·계정별 인증 조건, +이메일 별칭의 공급자/가입 수락, 개발자 가입 현행 화면, 한국 계정/OS별 예약 한도·라벨·음원 조합, 일반 독자 공개, 기기 전송·OS 설치 실증. 현재 수치·성공을 확정하지 않는다.\n')
    boxes=[]
    for index,p in enumerate(PAGES):
        x=20+(index%4)*155; y=30+(index//4)*110
        boxes.append(f'<rect x="{x}" y="{y}" width="140" height="80" rx="10" fill="{("#f3e8d6" if index in (8,9) else "#fffefa")}" stroke="#30624f"/><text x="{x+12}" y="{y+30}" font-size="18">실습 {index}</text><text x="{x+12}" y="{y+57}" font-size="14">{["시작 준비","계정·보안","설치","문안","카드","릴스","검수","앱 게시","선택 API","선택 예약","관찰"][index]}</text>')
    (SITE/'assets/img/practice/map.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 370" role="img" aria-labelledby="t"><title id="t">실습 0~10 학습 지도</title><rect width="650" height="370" fill="#eaf0e5"/><g font-family="system-ui,sans-serif" fill="#202d29">'+''.join(boxes)+'</g></svg>\n')
    print(f'실습 {len(PAGES)}개·E2E, 단계 {sum(len(p["steps"]) for p in PAGES)}개, 미확인 메뉴 {len(rows)}개 생성')


if __name__=='__main__':
    build()
