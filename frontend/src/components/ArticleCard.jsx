import { formatDate } from "../lib/format";

export default function ArticleCard({ article, bookmarked, onToggleBookmark, delay = 0 }) {
  return (
    <article
      className="article-enter rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
      style={{ animationDelay: `${Math.min(delay * 50, 400)}ms` }}
    >
      <div className="flex gap-4">
        <img
          src={
            article.thumbnail_url ||
            "/placeholder.png"
          }
          alt="기사 썸네일"
          className="hidden h-24 w-32 rounded-xl object-cover md:block"
        />

        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <a
              href={article.url}
              target="_blank"
              rel="noreferrer"
              className="line-clamp-2 text-base font-bold text-slate-900 hover:text-neon md:text-lg"
            >
              {article.title}
            </a>
            <button
              onClick={() => onToggleBookmark(article.id)}
              className={`whitespace-nowrap rounded-md border px-3 py-1 text-xs font-medium transition ${
                bookmarked
                  ? "border-slate-300 text-amber-400 hover:bg-slate-100"
                  : "border-slate-300 text-slate-500 hover:bg-slate-100"
              }`}
            >
              <span className="inline-flex items-center gap-1">
                <svg
                  className="h-3.5 w-3.5"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M7 3a2 2 0 0 0-2 2v16l7-4 7 4V5a2 2 0 0 0-2-2H7z" />
                </svg>
                스크랩
              </span>
            </button>
          </div>

          <p className="mt-2 line-clamp-3 text-sm text-slate-600">
            {article.description || "요약문이 없는 기사입니다."}
          </p>

          <p className="mt-3 text-xs text-slate-400">
            발행일 {formatDate(article.published_at)}
          </p>
        </div>
      </div>
    </article>
  );
}
