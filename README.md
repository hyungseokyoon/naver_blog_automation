# 블로그 자동화 (Blog Automation)

AI 콘텐츠 생성과 스텔스 브라우저 자동화를 사용하여 네이버 블로그 포스팅을 자동화하는 도구입니다.

## 🚀 개요
이 프로젝트는 Gemini AI를 활용한 고품질 콘텐츠 생성부터, 네이버 스마트에디터 ONE의 복잡한 브라우저 인터렉션까지 포스팅 전 과정을 자동화합니다.

## ✨ 주요 기능
- **AI 콘텐츠 생성**: Google Gemini 2.0 Flash를 활용한 SEO 최적화 글쓰기.
- **스텔스 자동화**: Playwright와 클립보드 기반 로그인을 사용하여 봇 감지 우회.
- **대량 처리**: 엑셀(Excel) 기반 데이터 소스를 통한 대량 포스팅 지원.
- **최신 에디터 지원**: 네이버 스마트에디터 ONE(블록 에디터) 맞춤형 로직.

## 🛠 기술 스택
- **Python**: 코어 로직 및 자동화 스크립트.
- **Playwright**: 최신 브라우저 자동화 엔진.
- **Google Generative AI**: 콘텐츠 생성을 위한 Gemini API.
- **BeautifulSoup4**: 콘텐츠 파싱 및 변환.
- **Openpyxl**: 대량 작업을 위한 엑셀 데이터 관리.

## 📦 설치 방법
1. 저장소 복제:
   ```bash
   git clone https://github.com/hyungseokyoon/blog_automation.git
   cd blog_automation
   ```
2. 가상환경 생성 및 활성화:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
4. `.env` 파일에 환경 변수 설정:
   ```env
   NAVER_ID=your_id
   NAVER_PW=your_password
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 📂 프로젝트 구조
- `src/auth/`: 로그인 및 세션 관리.
- `src/ai/`: Gemini 기반 콘텐츠 생성.
- `src/editor/`: 스마트에디터 ONE 인터렉션 로직.
- `src/parser/`: 데이터 입력 및 콘텐츠 매핑.
- `src/utils/`: 로깅 및 이미지 헬퍼 유틸리티.
- `data/`: 입력 데이터, 로그 및 브라우저 세션 저장.

## 📄 라이선스
MIT License
