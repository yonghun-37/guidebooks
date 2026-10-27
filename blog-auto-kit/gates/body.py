"""마크다운과 최종 HTML의 텍스트를 비교한다."""
from html.parser import HTMLParser
from content.markdown import render

class TextExtractor(HTMLParser):
    """HTML의 보이는 텍스트를 모은다."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def html_text(value):
    """태그를 제거하고 텍스트를 반환한다."""
    parser = TextExtractor(); parser.feed(value)
    return ' '.join(parser.parts)


def body_text(doc):
    """작성 원문과 최종 HTML을 함께 검사한다."""
    return doc.get('markdown', '') + '\n' + html_text(doc.get('html', ''))


def consistent(doc):
    """최종 HTML의 표시 텍스트가 원문과 같은지 확인한다."""
    expected = html_text(render(doc.get('markdown', '')))
    actual = html_text(doc.get('html', ''))
    return ' '.join(expected.split()) == ' '.join(actual.split())
