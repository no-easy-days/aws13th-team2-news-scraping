import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import ArticleList from './components/ArticleList';
import BookmarkSidebar from './components/BookmarkSidebar';
import { searchArticles, toggleBookmark } from './services/api';
import './App.css';

function App() {
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [bookmarkUpdate, setBookmarkUpdate] = useState(0);

  const handleSearch = async (keyword) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await searchArticles(keyword);
      if (result.status === 'success') {
        setArticles(result.data);
      } else if (result.status === 'NOT_FOUND') {
        setArticles([]);
        setError(result.message);
      }
    } catch (err) {
      setError('검색 중 오류가 발생했습니다.');
      setArticles([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBookmarkToggle = async (articleId) => {
    try {
      const result = await toggleBookmark(articleId);
      // 북마크 업데이트 시 사이드바 새로고침 트리거
      setBookmarkUpdate(prev => prev + 1);
      return result;
    } catch (err) {
      throw err;
    }
  };

  return (
    <div className="App">
      <BookmarkSidebar onBookmarkUpdate={bookmarkUpdate} />
      
      <header className="app-header">
        <h1>📰 매일경제 뉴스 검색</h1>
        <p>키워드로 기사를 검색하고 북마크하세요</p>
      </header>
      <SearchBar onSearch={handleSearch} />
      <ArticleList
        articles={articles}
        onBookmarkToggle={handleBookmarkToggle}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
}

export default App;
