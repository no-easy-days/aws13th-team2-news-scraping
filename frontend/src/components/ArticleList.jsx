import { useMemo, useState } from "react";
import ArticleCard from "./ArticleCard";

export default function ArticleList({ keyword, articles, loading, bookmarkIds, onToggleBookmark }) {
  const [sort, setSort] = useState("similarity");

  const sortedArticles = useMemo(() => {
    if (sort === "similarity") return articles;

    const copy = [...articles];
    if (sort === "latest") {
      copy.sort((a, b) => {
        const ad = new Date(a.published_at || a.created_at || 0).getTime();
        const bd = new Date(b.published_at || b.created_at || 0).getTime();
        return bd - ad;
      });
      return copy;
    }
    if (sort === "title") {
      copy.sort((a, b) => (a.title || "").localeCompare(b.title || "", "ko"));
      return copy;
    }
    return copy;
  }, [articles, sort]);

  if (loading) {
    return <div className="mt-6 text-sm text-slate-500">기사 목록을 불러오는 중입니다...</div>;
  }

  if (!articles.length) {
    return (
      <div className="mt-6 rounded-xl border border-dashed border-slate-300 p-6 text-sm text-slate-500">
        {keyword ? `"${keyword}" 관련 기사가 없습니다.` : "검색 결과가 없습니다."}
      </div>
    );
  }

  return (
    <section className="mt-6">
      <div className="mb-3 flex items-center justify-between text-xs text-slate-500">
        <p>결과 {articles.length}건</p>
        <div className="flex items-center gap-2">
          {[{ id: "similarity", label: "유사도" }, { id: "latest", label: "최신" }, { id: "title", label: "제목" }].map(
            (item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => setSort(item.id)}
                className={`rounded-xl border px-2.5 py-1 text-[11px] transition ${
                  sort === item.id
                    ? "border-sky-300 bg-sky-100 text-sky-700"
                    : "border-slate-300 bg-white text-slate-600 hover:border-sky-200 hover:text-sky-700"
                }`}
              >
                {item.label}
              </button>
            )
          )}
        </div>
      </div>
      <div className="grid gap-4">
        {sortedArticles.map((article, index) => (
          <ArticleCard
            key={article.id}
            article={article}
            delay={index}
            bookmarked={bookmarkIds.has(article.id)}
            onToggleBookmark={onToggleBookmark}
          />
        ))}
      </div>
    </section>
  );
}





