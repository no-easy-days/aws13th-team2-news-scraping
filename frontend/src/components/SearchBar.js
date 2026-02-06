import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch }) {
  const [keyword, setKeyword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (keyword.trim()) {
      onSearch(keyword.trim());
    }
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="기사 검색 키워드를 입력하세요..."
          className="search-input"
        />
        <button type="submit" className="search-button">
          검색
        </button>
      </form>
    </div>
  );
}

export default SearchBar;
