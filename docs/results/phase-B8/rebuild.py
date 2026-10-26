"""B8의 원고·출처 부록과 배포본을 재생성한다. 저장소 루트에서 실행."""
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_appendices_blog as book


def rebuild():
    book.build()
    site = ROOT / 'site-blog'
    kit = ROOT / 'blog-kit'
    out = site / 'samples/blog-kit'
    # 배포 README는 축약한 웹 미리보기 디렉터리의 실제 상대 주소를 쓴다.
    readme = (kit / 'README.md').read_text()
    for old, new in [('samples/rendered/preview.html', 'preview.html'),
                     ('samples/article.md', 'draft.md'), ('samples/routes.md', 'routes.md')]:
        readme = readme.replace(f']({old})', f']({new})')
    (out / 'README.md').write_text(readme)
    public = ['info-notes.txt', 'review-notes.txt', 'trip-notes.txt',
              'support-check.svg', 'review.md', 'trip.md', 'routes.md']
    for name in public:
        content = (kit / 'samples' / name).read_text()
        if name == 'routes.md':
            content = content.replace('](article.md)', '](draft.md)')
        (out / name).write_text(content)
    # 공통 배포기는 md/html/json/svg만 수집하므로 새 입력 메모 txt 3개만 명시 추가.
    with zipfile.ZipFile(out / 'blog-kit.zip', 'a') as archive:
        for name in public[:3]:
            info = zipfile.ZipInfo(f'blog-kit/samples/{name}', date_time=(2026, 10, 26, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (kit / 'samples' / name).read_bytes())
    # 공유 생성기와 다른 작업자의 파일을 고치지 않고 현재 용어집 정의를 보정한다.
    old = '광고 클릭당 비용·보고 단가입니다. 광고주의 입찰가를 내 광고 수입으로 바꾸지 않습니다.'
    new = '광고주가 지출한 광고비를 클릭 수로 나눈 값과 게시자 보고서의 클릭 단가를 구분합니다. 광고주 입찰가는 내 수입이 아닙니다. 블로그 운영자는 우선 자신의 예상 수입·페이지 RPM을 확인합니다.'
    glossary = site / 'glossary.html'
    assert old in glossary.read_text(), 'CPC 입력 정의 변경 여부 확인'
    for page in site.rglob('*.html'):
        text = page.read_text()
        if old in text:
            page.write_text(text.replace(old, new))
    # 배포된 실제 SVG 자산 이름을 이론의 완성 글 이미지에 연결한다.
    draft = (out / 'preview.html').read_text()
    asset = re.search(r'<img[^>]+src="(assets/[^"]+)"', draft)[1]
    chapter = site / 'chapters/06-writing.html'
    chapter.write_text(re.sub(r'src="../samples/blog-kit/assets/[^\"]+"',
                             f'src="../samples/blog-kit/{asset}"', chapter.read_text()))
    print('B8 웹 README·메모·ZIP·CPC 보정 완료')


if __name__ == '__main__':
    rebuild()
