import React, { useState } from 'react';
import './ArticleCard.css';

function ArticleCard({ article, onBookmarkToggle }) {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleBookmark = async () => {
    setIsLoading(true);
    try {
      const result = await onBookmarkToggle(article.id);
      setIsBookmarked(result.is_bookmarked);
    } catch (error) {
      console.error('북마크 처리 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="article-card">
      {article.thumbnail_url && (
        <div className="article-thumbnail">
          <img src={article.thumbnail_url} alt={article.title} />
        </div>
      )}
      <div className="article-content">
        <div className="article-header">
          <h3 className="article-title">{article.title}</h3>
          <button
            className={`bookmark-button ${isBookmarked ? 'bookmarked' : ''}`}
            onClick={handleBookmark}
            disabled={isLoading}
          >
            {isBookmarked ? '️🔫' : '🧨'}
          </button>
        </div>
        {article.data_score && (
          <div className="article-score">
            유사도: {(article.data_score * 100).toFixed(0)}%
          </div>
        )}
        <p className="article-summary">
          {article.description ? article.description.substring(0, 150) + '...' : '내용 없음'}
        </p>
        <div className="article-footer">
          <span className="article-date">{formatDate(article.published_at)}</span>
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="article-link"
          >
            기사 보기 →
          </a>
        </div>
      </div>
    </div>
  );
}

export default ArticleCard;
