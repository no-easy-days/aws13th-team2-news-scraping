import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# TODO: ORM 연결+pydantic, 디버깅 코드 로그 출력으로 변경, 중복 검사

def crawl_mk_news(days: int = 365) -> list[dict]:
    """
    매일경제 IT 뉴스를 크롤링합니다.

    Args:
        days: 오늘 기준 며칠 전까지 수집할지 (기본 365일 = 1년)

    Returns:
        기사 리스트 [{"title", "link", "description", "published_date", "thumbnail"}, ...]
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "Referer": "https://www.mk.co.kr/news/it",
    }
    # 쿠키 갱신 방법 (404 에러 발생 시):
    # 1. 브라우저에서 https://www.mk.co.kr/news/it 접속
    # 2. F12 → Network → "더보기" 클릭 → 요청 우클릭 → Copy as cURL
    # 3. 복사한 내용에서 PCID, SCOUTER 값 찾아서 아래 업데이트
    # * PCID는 JavaScript로 생성되어 requests로 자동 획득 불가
    cookies = {
        "PCID": "17683741249192596880095",
        "SCOUTER": "x391bqpj83qgof",
    }

    base_url = "https://www.mk.co.kr/_CP/855"
    cutoff_date = datetime.now() - timedelta(days=days)

    all_articles = []
    page = 1
    stop_crawling = False

    while not stop_crawling:
        params = {"page": page, "lcode": "it", "scode": "latest"}
        response = requests.get(base_url, params=params, headers=headers, cookies=cookies)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("li.article_list")

        if not articles:
            break

        for article in articles:
            parsed = _parse_article(article)
            if not parsed:
                continue

            if parsed["_date_obj"] < cutoff_date:
                stop_crawling = True
                break

            del parsed["_date_obj"]
            all_articles.append(parsed)

        page += 1
        time.sleep(1.0)

    return all_articles


def _parse_article(article) -> dict | None:
    """기사 하나를 파싱. 실패하면 None."""
    link_tag = article.select_one("a.news_item")
    title_tag = article.select_one("h4")
    desc_tag = article.select_one("p.art_desc")
    time_area = article.select_one("div.time_area span")
    img_tag = article.select_one("div.list_thumb img")

    article_date = None
    if time_area:
        date_text = time_area.get_text(separator=" ", strip=True)
        parts = date_text.split()
        if len(parts) == 2:
            try:
                article_date = datetime.strptime(f"{parts[1]}.{parts[0]}", "%Y.%m.%d")
            except ValueError:
                print(f"날짜 파싱 실패: {date_text}")

    if not (link_tag and title_tag and article_date):
        return None

    return {
        "title": title_tag.get_text(strip=True),
        "link": link_tag.get("href"),
        "description": desc_tag.get_text(strip=True) if desc_tag else "",
        "date": article_date.strftime("%Y-%m-%d"),
        "thumbnail": img_tag.get("src") if img_tag else "",
        "_date_obj": article_date,
    }


if __name__ == "__main__":
    print("매일경제 IT 뉴스 크롤링 시작...\n")
    articles = crawl_mk_news(days=7)  # 테스트: 7일치

    print(f"\n총 {len(articles)}개 수집 완료\n")

    print("=== 최신 기사 5개 ===")
    for i, a in enumerate(articles[:5], 1):
        print(f"{i}. [{a['date']}] {a['title']}")

    print("\n=== 가장 오래된 기사 5개 ===")
    for i, a in enumerate(articles[-5:], 1):
        print(f"{i}. [{a['date']}] {a['title']}")
