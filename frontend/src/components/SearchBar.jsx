import { useEffect, useState } from "react";

export default function SearchBar({ defaultKeyword, loading, crawling, onSearch, onCrawl }) {
  const [input, setInput] = useState(defaultKeyword);

  useEffect(() => {
    setInput(defaultKeyword);
  }, [defaultKeyword]);

  const submit = (event) => {
    event.preventDefault();
    onSearch(input);
  };

  return (
    <form onSubmit={submit} className="rounded-2xl border border-slate-200 bg-slate-50 p-3 md:p-4">
      <div className="flex flex-col gap-3 md:flex-row">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="예: 테크, 인공지능, 클라우드, 보안"
          className="h-12 flex-1 rounded-xl border border-slate-300 bg-white px-4 text-sm outline-none transition focus:border-neon"
        />
        <div className="flex gap-2">
          <button
            type="submit"
            disabled={loading}
            className="h-12 min-w-24 rounded-xl bg-ink px-4 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:opacity-60"
          >
            {loading ? "검색 중" : "검색"}
          </button>
          {/* <button
            type="button"
            disabled={crawling}
            onClick={onCrawl}
            className="h-12 min-w-24 rounded-xl bg-neon px-4 text-sm font-semibold text-white transition hover:bg-sky-500 disabled:opacity-60"
          >
            {crawling ? "실행 중" : "크롤링"}
          </button> */}
        </div>
      </div>
    </form>
  );
}
