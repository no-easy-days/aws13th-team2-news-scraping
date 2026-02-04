# aws13th-team2-news-scraping

### 프로젝트 시작 방법
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
4. 환경변수 파일(.env) 생성 및 설정
   ```plaintext
   DB_URL=your_db_url
   ```
5. 실행
    ```bash
    fastapi dev main.py
    ```