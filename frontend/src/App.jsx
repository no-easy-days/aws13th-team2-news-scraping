import { useEffect, useMemo, useState } from "react";
import { crawlArticles, fetchArticles, fetchBookmarks, toggleBookmark } from "./lib/api";
import SearchBar from "./components/SearchBar";
import ArticleList from "./components/ArticleList";
import BookmarkSidebar from "./components/BookmarkSidebar";

const QUICK_KEYWORDS = ["테크", "인공지능", "제약·바이오", "과학", "우주", "건강"];

export default function App() {
  const [keyword, setKeyword] = useState("");
  const [articles, setArticles] = useState([]);
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [crawling, setCrawling] = useState(false);
  const [isScrapOpen, setIsScrapOpen] = useState(false);
  const [message, setMessage] = useState("키워드를 입력하면 관련 기사 결과가 바로 표시됩니다.");

  const bookmarkIds = useMemo(
    () => new Set(bookmarks.map((item) => item.article?.id ?? item.article_id ?? item.id)),
    [bookmarks]
  );

  async function handleSearch(nextKeyword) {
    const clean = nextKeyword.trim();
    if (!clean) {
      setMessage("검색어를 입력해 주세요.");
      return;
    }

    setKeyword(clean);
    setLoading(true);
    setMessage("검색 중...");
    try {
      const response = await fetchArticles(clean);
      const data = response?.data ?? [];
      setArticles(data);
      setMessage(
        data.length
          ? `"${clean}" 검색 결과 ${data.length}건`
          : `"${clean}" 관련 결과가 없습니다.`
      );
    } catch (error) {
      setMessage(error.message || "검색 요청 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  }

  async function loadBookmarks() {
    try {
      const response = await fetchBookmarks();
      setBookmarks(response?.data ?? []);
    } catch {
      setBookmarks([]);
    }
  }

  async function handleToggleBookmark(articleId) {
    try {
      await toggleBookmark(articleId);
      await loadBookmarks();
    } catch (error) {
      setMessage(error.message || "북마크 처리 중 오류가 발생했습니다.");
    }
  }

  async function handleRemoveBookmark(articleId) {
    if (!articleId) return;
    await handleToggleBookmark(articleId);
  }

  async function handleCrawl() {
    setCrawling(true);
    setMessage("크롤링 실행 중...");
    try {
      await crawlArticles();
      setMessage("크롤링 완료. 현재 키워드로 목록을 갱신합니다.");
      await handleSearch(keyword);
    } catch (error) {
      setMessage(error.message || "크롤링 API 준비 후 다시 시도해 주세요.");
    } finally {
      setCrawling(false);
    }
  }

  useEffect(() => {
    loadBookmarks();
  }, []);

  return (
    <div className="grid-overlay min-h-screen px-4 py-8 md:px-8">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1fr_320px]">
        <main className="rounded-3xl border border-white/50 bg-white/80 p-5 shadow-float backdrop-blur md:p-8">
          <header className="mb-6 space-y-3">
            <p className="inline-flex rounded-full bg-coral/15 px-3 py-1 text-xs font-semibold text-coral">
              IT 뉴스 검색 아카이브
            </p>
            <h1 className="text-2xl font-bold tracking-tight md:text-4xl">매일 경제 뉴스 검색</h1><br></br>
            {/* <p className="text-sm text-slate-600 md:text-base">매일 경제 테크 과학 기사 검색 엔진입니다.</p> */}
            <div className="flex flex-wrap gap-2">
              {QUICK_KEYWORDS.map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => handleSearch(item)}
                  className="rounded-full border border-slate-300 bg-white px-3 py-1 text-xs text-slate-700 transition hover:border-neon hover:text-neon"
                >
                  #{item}
                </button>
              ))}
            </div>
          </header>

          <SearchBar
            defaultKeyword={keyword}
            loading={loading}
            crawling={crawling}
            onSearch={handleSearch}
            onCrawl={handleCrawl}
          />

          <div className="mt-4 rounded-xl bg-slate-900 px-4 py-2 text-sm text-slate-100">{message}</div>

          <ArticleList
            keyword={keyword}
            articles={articles}
            loading={loading}
            bookmarkIds={bookmarkIds}
            onToggleBookmark={handleToggleBookmark}
          />
        </main>

        <BookmarkSidebar
          bookmarks={bookmarks}
          onRemoveBookmark={handleRemoveBookmark}
          className="hidden lg:flex"
        />
      </div>

      <button
        type="button"
        onClick={() => setIsScrapOpen(true)}
        className="fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white/90 px-4 py-2 text-sm font-semibold text-slate-700 shadow-lg backdrop-blur lg:hidden"
      >
        스크랩
      </button>

      {isScrapOpen ? (
        <div className="fixed inset-0 z-50 lg:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-black/30"
            onClick={() => setIsScrapOpen(false)}
            aria-label="뒤로"
          />
          <div className="absolute right-4 top-16 w-[min(90vw,360px)]">
            <BookmarkSidebar
              bookmarks={bookmarks}
              onRemoveBookmark={handleRemoveBookmark}
              onClose={() => setIsScrapOpen(false)}
              className="max-h-[70vh]"
            />
          </div>
        </div>
      ) : null}
    </div>
  );
}
