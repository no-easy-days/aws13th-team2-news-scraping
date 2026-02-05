import logging
import random
import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from schemas.article import ArticleCreate
from database import SessionLocal
from repositories.article_repository import ArticleRepository

logger = logging.getLogger(__name__)


def crawl_mk_news(days: int = 365) -> list[ArticleCreate]:
    """
    매일경제 IT 뉴스를 크롤링합니다.

    Args:
        days: 오늘 기준 며칠 전까지 수집할지 (기본 365일 = 1년)

    Returns:
        ArticleCreate 스키마 리스트

    Note:
        - API가 최신순 정렬을 보장한다는 전제 하에 동작
        - 정렬이 바뀌면 cutoff_date 기반 중단 로직이 오작동할 수 있음
    """
    logger.info("매일경제 IT 뉴스 크롤링 시작 (최근 %d일)", days)

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

    all_articles: list[ArticleCreate] = []
    page = 1
    stop_crawling = False

    while not stop_crawling:
        params = {"page": page, "lcode": "it", "scode": "latest"}

        # 최대 3회 재시도
        response = None
        for attempt in range(3):
            try:
                response = requests.get(base_url, params=params, headers=headers, cookies=cookies, timeout=10)
                if response.status_code == 200:
                    break

                logger.error(
                    "Page %s 요청 실패 (%s), 재시도 %s/3",
                    page, response.status_code, attempt + 1
                )
            except requests.RequestException as e:
                logger.error(
                    "Page %s 네트워크 오류 (%s), 재시도 %s/3",
                    page, e, attempt + 1
                )
            time.sleep(2)
        else:
            # 3회 모두 실패
            logger.error(
                "Page %s 요청 최종 실패, 크롤링 중단",
                page
            )
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("li.article_list")

        if not articles:
            break

        for article in articles:
            parsed = _parse_article(article)
            if parsed is None:
                continue

            if parsed.published_at < cutoff_date:
                stop_crawling = True
                break

            all_articles.append(parsed)

        # 진행 상황 출력
        oldest = all_articles[-1].published_at.strftime("%Y-%m-%d") if all_articles else "-"
        logger.info(
            "Page %s: %s개 수집 | 마지막 기사: %s",
            page, len(all_articles), oldest
        )

        page += 1
        time.sleep(random.uniform(0.5, 1.0))

    return all_articles


def _parse_article(article) -> ArticleCreate | None:
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
                logger.warning(
                    "날짜 파싱 실패: %s",
                    date_text
                )

    if not (link_tag and title_tag and article_date):
        return None

    try:
        return ArticleCreate(
            title=title_tag.get_text(strip=True),
            url=link_tag.get("href"),
            description=desc_tag.get_text(strip=True) if desc_tag else None,
            published_at=article_date,
            thumbnail_url=img_tag.get("src") if img_tag else None,
        )
    except Exception as e:
        logger.error("Pydantic 검증 실패: %s", e)
        return None


def save_to_db(articles: list[ArticleCreate]) -> tuple[int, int]:
    """
    크롤링한 기사들을 DB에 저장합니다.

    Args:
        articles: ArticleCreate 리스트

    Returns:
        (성공 개수, 중복 개수)
    """

    db = SessionLocal()
    try:
        repo = ArticleRepository(db)
        return repo.bulk_create(articles)
    finally:
        db.close()
