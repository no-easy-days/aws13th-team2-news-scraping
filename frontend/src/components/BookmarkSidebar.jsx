export default function BookmarkSidebar({ bookmarks, onRemoveBookmark, className = "", onClose }) {
  return (
    <aside className={`sticky top-6 self-start flex max-h-[calc(100vh-3rem)] flex-col rounded-3xl border border-sky-100 bg-white/80 p-5 text-slate-800 shadow-float backdrop-blur md:p-6 ${className}`}>
      <div className="mb-3 flex items-center justify-between">
        <div>
          <p className="mb-2 inline-flex self-start rounded-full bg-sky-100 px-2.5 py-1 text-[11px] font-semibold text-sky-700">
            스크랩
          </p>
          <h2 className="text-lg font-bold">북마크 목록</h2>
        </div>
        {onClose ? (
          <button
            type="button"
            onClick={onClose}
            className="rounded-md border border-slate-200 px-2 py-1 text-xs text-slate-500 hover:border-slate-300 hover:text-slate-700"
          >
            닫기
          </button>
        ) : null}
      </div>

      <div className="flex-1 overflow-y-auto pr-1">
        {!bookmarks.length ? (
          <div className="rounded-xl border border-dashed border-sky-100 bg-sky-50/60 p-4 text-sm text-slate-500">
            아직 북마크한 기사가 없습니다.
          </div>
        ) : (
          <ul className="space-y-2.5">
            {bookmarks.slice(0, 15).map((item) => (
              <li
                key={item.bookmark_id ?? `${item.user_id ?? "u"}-${item.article_id ?? item.id}`}
                className="rounded-xl border border-sky-100 bg-sky-50/70 px-3 py-2.5 text-sm text-slate-700 transition hover:border-sky-200 hover:bg-sky-50"
              >
                <div className="flex items-center justify-between gap-2">
                  <a
                    href={item.article?.url}
                    target="_blank"
                    rel="noreferrer"
                    className="line-clamp-1 text-sm font-medium text-slate-800 hover:text-neon"
                  >
                    {item.article?.title ?? "제목 없음"}
                  </a>
                  <button
                    type="button"
                    onClick={() => onRemoveBookmark?.(item.article?.id)}
                    className="h-6 w-12 shrink-0 whitespace-nowrap rounded-md border border-slate-200 text-[10px] text-slate-500 hover:border-slate-300 hover:text-slate-700"
                  >
                    삭제
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </aside>
  );
}
