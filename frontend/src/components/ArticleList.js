import React from 'react';
import ArticleCard from './ArticleCard';
import './ArticleList.css';

function ArticleList({ articles, onBookmarkToggle, isLoading, error }) {
  if (isLoading) {
    return <div className="loading">검색 중...</div>;
  }

  if (error) {
    return <div className="error">오류가 발생했습니다: {error}</div>;
  }

  if (!articles || articles.length === 0) {
    return <div className="no-results">검색 결과가 없습니다.</div>;
  }

  return (
    <div className="article-list">
      <div className="article-count">
        총 {articles.length}개의 기사를 찾았습니다.
      </div>
      {articles.map((article) => (
        <ArticleCard
          key={article.id}
          article={article}
          onBookmarkToggle={onBookmarkToggle}
        />
      ))}
    </div>
  );
}

export default ArticleList;
