# aws13th-team2-news-scraping
**뉴스 스크래핑 및 조회 웹 애플리케이션 (FastAPI + React)**

## 프로젝트 시작 방법
1. 저장소 클론
   ```bash
   git clone git@github.com:no-easy-days/aws13th-team2-news-scraping.git
   ```
2. 가상환경 생성 및 활성화
   ```bash
    python -m venv venv
    source venv/bin/activate        # MacOS/Linux
    source .venv/Scripts/activate    # Windows
     ```
3. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```
4. 환경변수 파일 생성 및 설정
- /.env
   ```plaintext
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   ```
  
6. 실행
    ```bash
    uvicorn main:app --reload
    cd frontend && npm install && npm run dev
    ```
    
## 시스템 아키텍처
<img width="1680" height="862" alt="image" src="https://github.com/user-attachments/assets/8f541821-9dc9-432d-9c19-d0b57859c0ed" />


## ERD
<img width="1700" height="1000" alt="image" src="https://github.com/user-attachments/assets/a5df6275-ff3d-4bbe-b102-54142452b222" />

## 시연 페이지
### 홈페이지
<img width="1681" height="764" alt="Screenshot 2026-02-06 at 16 59 31" src="https://github.com/user-attachments/assets/24516510-3637-4f9e-9fab-f562e0c79c4c" />
<br><br><br>

### 검색 및 북마크
<img width="1673" height="962" alt="Screenshot 2026-02-06 at 17 00 05" src="https://github.com/user-attachments/assets/ea4c7deb-9d36-455f-a52b-5ada3c54aa94" />
