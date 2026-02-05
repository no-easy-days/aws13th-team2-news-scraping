import React, { useState, useEffect } from 'react';
import { getBookmarks, toggleBookmark } from '../services/api';
import './BookmarkSidebar.css';

function BookmarkSidebar({ onBookmarkUpdate }) {
  const [bookmarks, setBookmarks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(true);

  const fetchBookmarks = async () => {
    setIsLoading(true);
    try {
      const result = await getBookmarks();
      if (result.status === 'success') {
        setBookmarks(result.data);
      }
    } catch (error) {
      console.error('북마크 목록 로딩 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBookmarks();
  }, [onBookmarkUpdate]);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const handleRemoveBookmark = async (e, articleId) => {
    e.preventDefault(); // 링크 이동 방지
    e.stopPropagation(); // 이벤트 버블링 방지
    
    try {
      await toggleBookmark(articleId);
      // 삭제 후 목록 새로고침
      fetchBookmarks();
    } catch (error) {
      console.error('북마크 삭제 실패:', error);
      alert('북마크 삭제에 실패했습니다.');
    }
  };

  return (
    <>
      <button 
        className={`sidebar-toggle ${isOpen ? 'open' : ''}`}
        onClick={toggleSidebar}
      >
        {isOpen ? '🐽 닫기' : '️🐽'}
      </button>
      
      <div className={`bookmark-sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h3>내 북마크</h3>
          <span className="bookmark-count">{bookmarks.length}</span>
        </div>
        
        {isLoading ? (
          <div className="sidebar-loading">로딩 중...</div>
        ) : bookmarks.length === 0 ? (
          <div className="sidebar-empty">
            북마크한 기사가 없습니다.
          </div>
        ) : (
          <ul className="bookmark-list">
            {bookmarks.map((item) => (
              <li key={item.bookmark_id} className="bookmark-item">
                <a 
                  href={item.article.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="bookmark-link"
                >
                  <div className="bookmark-content">
                    <div className="bookmark-title">{item.article.title}</div>
                    <div className="bookmark-date">
                      {new Date(item.bookmarked_at).toLocaleDateString('ko-KR')}
                    </div>
                  </div>
                </a>
                <button 
                  className="bookmark-remove"
                  onClick={(e) => handleRemoveBookmark(e, item.article.id)}
                  title="북마크 삭제"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
}

export default BookmarkSidebar;
