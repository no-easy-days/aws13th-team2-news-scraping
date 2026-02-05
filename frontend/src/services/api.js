const API_BASE_URL = 'http://localhost:8000';

export const searchArticles = async (keyword) => {
  try {
    const response = await fetch(`${API_BASE_URL}/articles?keyword=${encodeURIComponent(keyword)}`);
    if (!response.ok) {
      throw new Error('검색에 실패했습니다.');
    }
    return await response.json();
  } catch (error) {
    console.error('Error searching articles:', error);
    throw error;
  }
};

export const toggleBookmark = async (articleId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/articles/${articleId}/bookmark`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('북마크 처리에 실패했습니다.');
    }
    return await response.json();
  } catch (error) {
    console.error('Error toggling bookmark:', error);
    throw error;
  }
};

export const getBookmarks = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/articles/bookmarks`);
    if (!response.ok) {
      throw new Error('북마크 목록 조회에 실패했습니다.');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching bookmarks:', error);
    throw error;
  }
};
