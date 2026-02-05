# 1. 텍스트를 조각내는 도구
def make_ngram(text: str, n=2):
    text = text.replace(" ", "").lower()
    return [text[i:i + n] for i in range(len(text) - n + 1)]


def get_similarity(query: str, target: str):
    """두 텍스트 간의 자카드 유사도를 계산하는 함수"""
    search_bar = set(make_ngram(query)) # 검색어 짜르기
    title = set(make_ngram(target))    # 제목 짜르기

    # 만약 빈 집합이면
    if not search_bar or not title:
        return 0.0

    intersection = search_bar & title # 즉 공통점이 몇 개 인지
    union = search_bar | title # 전체 범위 파악 할려고

    return len(intersection) / len(union) # 전체에서 공통점이 몇개인지 점수화
