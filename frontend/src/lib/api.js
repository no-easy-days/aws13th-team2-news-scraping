const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : detail?.message || data?.message || "Request failed.";
    throw new Error(message);
  }

  return data;
}

export function fetchArticles(keyword) {
  const query = new URLSearchParams({ keyword }).toString();
  return request(`/articles?${query}`);
}

export function toggleBookmark(articleId) {
  return request(`/articles/${articleId}/bookmark`, { method: "POST" });
}

export function crawlArticles() {
  return request("/articles/crawl", { method: "POST" });
}

export function fetchBookmarks() {
  return request("/articles/bookmarks");
}
