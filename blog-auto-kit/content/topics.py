"""월령과 주제별 글감 지도를 만든다."""
def build_topics(today: str) -> dict:
    """고정 기준일을 포함한 글감 지도를 반환한다."""
    return {'as_of': today, 'topics': [
        {'category': '월령', 'title': '월령으로 찾는 집 놀이', 'age_range': '0~3세'},
        {'category': '발달', 'title': '개인차를 이해하고 공식 발달 안내 찾기', 'age_range': '0~3세'},
        {'category': '제도', 'title': '부모급여와 아동수당', 'age_range': '0~3세'},
        {'category': '놀이', 'title': '생후 3~4개월 터미타임', 'age_range': '3~4개월'},
        {'category': '제품', 'title': '손톱 관리 도구 비교', 'age_range': '0~3세'},
        {'category': '그림책', 'title': '아이와 책 정리하기', 'age_range': '0~3세'}]}
