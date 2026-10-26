"""직접 설계한 시스템 그림을 라이트/다크 SVG로 재생성한다."""
from html import escape
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import ROOT

def draw(name,title,subtitle,nodes,edges,notes):
    directory=ROOT/'docs/figures';directory.mkdir(parents=True,exist_ok=True)
    for dark in (False,True):
        bg,fg,panel,accent,muted=('#111d29','#edf5fa','#22384b','#70d6bd','#b1c1d0') if dark else ('#f6f3eb','#153b42','#ffffff','#18765d','#546a74')
        pieces=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1100 680" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle+" "+" ".join(notes))}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="{accent}"/></marker></defs><rect width="1100" height="680" rx="18" fill="{bg}"/><g font-family="system-ui,sans-serif" fill="{fg}"><text x="40" y="55" font-size="30" font-weight="700">{escape(title)}</text><text x="40" y="90" font-size="17" fill="{muted}">{escape(subtitle)}</text>']
        for x1,y1,x2,y2,label in edges:
            pieces.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{accent}" stroke-width="3" marker-end="url(#arrow)"/><text x="{(x1+x2)/2+4}" y="{(y1+y2)/2-8}" font-size="15" fill="{muted}">{escape(label)}</text>')
        for x,y,w,h,title_,lines,link in nodes:
            pieces.append(f'<a xlink:href="{escape(link)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{panel}" stroke="{accent}" stroke-width="2"/><text x="{x+18}" y="{y+32}" font-size="18" font-weight="700">{escape(title_)}</text>')
            for i,line in enumerate(lines):pieces.append(f'<text x="{x+18}" y="{y+61+i*25}" font-size="17">{escape(line)}</text>')
            pieces.append('</a>')
        for i,line in enumerate(notes):pieces.append(f'<text x="40" y="{575+i*27}" font-size="17" fill="{muted}">{escape(line)}</text>')
        pieces.append('</g></svg>')
        (directory/(name+('-dark' if dark else '')+'.svg')).write_text(''.join(pieces),encoding='utf-8')

def box(x,y,title,lines,link='../../README.md',w=280,h=120):return (x,y,w,h,title,lines,link)

def main():
    draw('system','주제에서 다음 주제까지','두 흐름은 상태·비용·관문을 공유하고 게시 API만 나눕니다.',[
      box(40,140,'① 소스 + 지난 성과',['하린: 청년 지원금 체크','도윤: 월급날 네 칸 메모']),box(410,140,'② 생성 API',['대상·기간·서류 → 카드','월세·생활비 등 → 대본']),box(780,140,'③ 코드 렌더',['Pillow PNG/JPEG','ffmpeg MP4·자막·음량']),
      box(780,370,'④ 관문 + 운영 모드',['사실·정책·유사도·규격·비용','auto / post_review / approval']),box(410,370,'⑤ 게시 + 지표',['Instagram 공개 URL·컨테이너','YouTube 동일 세션 재개']),box(40,370,'⑥ SQLite + 비용',['상태·파일 해시·발행 ID','지표 재조회 → 주제 점수'])],[(320,200,400,200,''),(690,200,770,200,''),(920,260,920,360,''),(780,430,700,430,''),(410,430,330,430,''),(180,370,180,270,'다음 날')],['mock: 외부 호출 0 · live: 사용자 키·인증 파일 필요','비밀·DB는 private/ · 공개 버킷에는 게시용 JPEG/MP4만'])
    draw('timeline','하루의 자동 실행 타임라인','시각은 키트 운영 예입니다. OS 현지 시각, 예약 간격 15분 기본값.',[
      box(40,150,'09:17 새 콘텐츠',['주제 → 생성 → 렌더','하루 새 실행은 1회']),box(410,150,'09:17 품질 관문',['통과 → 모드별 진행','실패 → 이유와 알림']),box(780,150,'공개 전 2시간',['사후 확인 기본값','거부 시 예약 취소']),
      box(40,380,'15분마다 tick',['실패/연기 단계 재개','승인 대기는 바로 종료']),box(410,380,'다음 날 지표 재조회',['최근 게시물 기본 7일','미준비와 0 구분']),box(780,380,'일일 운영 보고',['비용·예외·실행 이력','대시보드·알림'])],[(320,210,400,210,''),(690,210,770,210,''),(180,270,180,370,''),(320,440,400,440,''),(690,440,770,440,'')],['처음에는 approval → 기준을 조정한 뒤 auto로 전환','지연·절전·한도 때문에 정시 실행은 보장되지 않습니다.'])
    draw('sequence','게시 API 호출 순서','인증 값은 항상 가립니다. 토큰·개인 업로드 Location을 로그에 쓰지 않습니다.',[
      box(40,140,'Instagram ①',['계정 한도 조회','JPEG/릴스 URL → media']),box(410,140,'Instagram ②',['컨테이너 ID 저장','status_code 반복 조회']),box(780,140,'Instagram ③',['FINISHED → media_publish','게시 ID를 즉시 저장']),
      box(40,380,'YouTube ①',['private·AI·아동용·예약','POST → Location 비공개 저장']),box(410,380,'YouTube ②',['PUT 청크 → 308 Range','다음 바이트부터 계속']),box(780,380,'YouTube ③',['200/201 → 영상 ID 저장','끊기면 같은 Location 조회'])],[(320,200,400,200,''),(690,200,770,200,''),(320,440,400,440,''),(690,440,770,440,'')],['POST 결과 불명 → 새 게시 요청 금지 · 기존 컨테이너/세션 조회','Instagram PUBLISHED인데 ID가 없으면 reconcile로 계정의 기존 ID를 대조'])
    draw('states','실행 상태와 재시작','완료한 단계는 건너뛰고 실패 단계부터 이어갑니다.',[
      box(40,140,'running',['topic → budget → draft','render → host → gates']),box(410,140,'waiting_approval',['approve ID','파일/대상/예약을 해시 결합']),box(780,140,'done / dry_run',['발행 ID / 요청 계획 저장','insights → 성과 반영']),
      box(40,380,'failed / deferred',['실패: 같은 ID resume','한도: 시각이 되면 tick']),box(410,380,'exception / rejected',['관문 이유 확인 후 새 실행','거부한 실행은 발행 안 함']),box(780,380,'uncertain / scheduled',['불명: 조회·수동 ID 대조','예약: 공개 전 거부 가능'])],[(320,200,400,200,'승인제'),(690,200,770,200,'승인'),(180,260,180,370,'실패/한도'),(550,260,550,370,'변경/거부'),(920,260,920,370,'유실/예약')],['auto는 통과 즉시 게시 · Instagram 사후 확인은 로컬 발행 대기','게시 저널·업로드 세션·중복 해시는 재시작 뒤에도 유지합니다.'])
    draw('gates','품질 관문 판정','자동 관문은 검사 가능한 신호를 찾습니다. 사실·권리 전체 보장은 아닙니다.',[
      box(40,140,'사실·정책',['확인할 3가지: 원문 대조','지원금 99만원: 숫자 실패']),box(410,140,'중복·반복',['문자 n-gram Jaccard','최근 게시물과 비교']),box(780,140,'규격·AI·비용',['ffprobe/ffmpeg·LUFS','Boolean 표시·비용 상한']),
      box(40,380,'한 항목이라도 실패',['exception + 이유 저장','로컬·메신저 미리보기']),box(410,380,'모든 항목 통과',['auto: 게시','approval: 승인 대기']),box(780,380,'사후 확인 모드',['미래 시각으로 예약','거부 전 공개 여부 확인'])],[(320,200,400,200,''),(690,200,770,200,''),(180,260,180,370,'실패'),(550,260,550,370,'통과'),(920,260,920,370,'통과')],['유사도 0.82, 음량 -19~-13 LUFS: 키트 기본값(바꿀 수 있음)','이름 누락·문맥 오류는 놓칠 수 있습니다. 선택 LLM 대조도 별도 비용입니다.'])
    draw('folders','폴더와 설정의 연결','설정에는 선택·상한을, .env에는 비밀을, private에는 실행 상태를 둡니다.',[
      box(40,140,'config.json',['mode / providers / models','budget / gates / hosting']),box(410,140,'.env + private 인증',['API 키·사용자 토큰','Git/공개 URL에 넣지 않기']),box(780,140,'providers/prices.json',['2026-10-26 조사 단가','모델·단가·근거 분리']),
      box(40,380,'private/state/실행ID/',['draft·config·미디어·승인','컨테이너/업로드 저널']),box(410,380,'state.sqlite',['단계·예외·비용·해시','지표와 Telegram offset']),box(780,380,'공개 미디어 호스팅',['번호가 붙은 JPEG/MP4','설정/토큰/DB 업로드 금지'])],[(180,260,180,370,''),(550,260,550,370,''),(690,200,770,200,'견적'),(690,440,770,440,'미디어만')],['카드·렌더·업로드 코드는 기존 키트에서 복사해 독립 실행','Actions는 암호화된 외부 상태와 미완료 lease를 사용합니다.'])
    draw('costs','비용 상한과 게시 한도','금액 예시는 키트 설정값이며 서비스 무료량을 보장하지 않습니다.',[
      box(40,140,'일 비용 상한 $1',['실행 전체 최대비 예약','호출마다 예약 안에서 차감']),box(410,140,'월 비용 상한 $10',['재시도·불명 비용 포함','상한 초과 전 중단·알림']),box(780,140,'실제 usage 기록',['tokens / 문자 / 영상 초','누락 시 최대 예약액 유지']),
      box(40,380,'Instagram 계정 한도',['조회 성공: usage / total','조회 실패: 미확인 → 연기']),box(410,380,'YouTube 할당량',['Console 확인 + 로컬 cap','403/429 제한이면 연기']),box(780,380,'지출 예산 ≠ 클라우드 알림',['공급자 hard cap도 설정','호스팅·세금·구독 별도'])],[(320,200,400,200,''),(690,200,770,200,''),(320,440,400,440,''),(690,440,770,440,'')],['실제 사용량 차트와 quota 스냅샷은 private/state/dashboard.html','이미지·영상 생성 활성화 시 실행 최대비가 커집니다. 상한을 먼저 확인하세요.'])
    draw('alerts','대시보드와 승인·예외 알림 예','아래 실행 ID와 비용은 설명용 가상 예입니다.',[
      box(40,140,'대시보드',['청년 지원금 체크 · 승인 대기','관문 ✓ · 생성비 $0.0008']),box(410,140,'승인 알림 + 이미지',['미리보기 / 문안 확인','Telegram 승인·거부 버튼']),box(780,140,'예외 알림 + 이유',['지원금 99만원 → 예외','원문에 없는 숫자: 99']),
      box(40,380,'비용·quota',['일/월 사용 막대','미확인 / 사용 / 총량']),box(410,380,'지표와 준비 상태',['views 0회: available','reach 빈 값: missing']),box(780,380,'안전한 승인 경로',['로컬 approve ID','Discord는 알림만'])],[(320,200,400,200,''),(690,200,770,200,''),(320,440,400,440,''),(690,440,770,440,'')],['문안은 직접 작성한 예시 · 실제 제도명·금액은 넣지 않음','Telegram: 허용 사용자·chat·해시·중복 확인 · 키/토큰은 알림에서 제외'])
    print('라이트/다크 SVG 16개 생성 완료')

if __name__=='__main__':main()
