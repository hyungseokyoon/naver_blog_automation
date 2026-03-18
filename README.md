# 블로그 자동화 (Blog Automation)

AI 콘텐츠 생성과 스텔스 브라우저 자동화를 사용하여 네이버 및 워드프레스 블로그 포스팅을 자동화하는 도구입니다.

## 🚀 개요
이 프로젝트는 Gemini AI를 활용한 고품질 콘텐츠 생성부터, 네이버 스마트에디터 ONE의 복잡한 브라우저 인터렉션까지 포스팅 전 과정을 자동화합니다.

## ✨ 주요 기능
- **AI 콘텐츠 생성**: 폴더 내 이미지를 분석하여 SEO 최적화된 블로그 포스트를 자동으로 생성합니다.
- **멀티 플랫폼 지원**: 네이버 블로그와 워드프레스(준비 중)를 하나의 도구로 관리합니다.
- **스텔스 자동화**: Playwright와 실제 키보드 타이핑 모방을 통해 봇 감지를 효과적으로 우회합니다.
- **세션 유지**: 한 번 로그인하면 세션을 저장하여 매번 로그인할 필요 없이 즉시 포스팅합니다.
- **최신 에디터 지원**: 네이버 스마트에디터 ONE(블록 에디터) 맞춤형 이미지/텍스트 블록 삽입 로직.

## 📦 설치 및 설정
1. 저장소 복제 및 의존성 설치:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
2. `.env` 파일 설정:
   ```env
   NAVER_ID=아이디
   NAVER_PW=비밀번호
   NAVER_BLOG_ID=블로그_아이디 (아이디와 다른 경우)
   GEMINI_API_KEY=제미나이_API_키
   ```

## 🛠 사용 방법

### 1단계: 콘텐츠 생성 (Generate)
`data/inputs/naver/{폴더명}` 경로에 포스팅에 사용할 사진들을 넣습니다.
```bash
python main.py --generate --platform naver --folder trip_to_jeju
```
Gemini가 사진을 분석하여 `post.json` 파일을 해당 폴더에 만들어줍니다.

### 2단계: 블로그 발행 (Write)
생성된 `post.json` 내용을 바탕으로 실제 블로그에 업로드합니다.
```bash
python main.py --write --platform naver --folder trip_to_jeju
```

### 기타 명령어
- **최신 글 목록 확인**: `python main.py --list --platform naver`
- **단순 텍스트 테스트**: `python main.py --write --title "제목" --content "내용"`

## 📂 프로젝트 구조
- `src/auth/`: 로그인 및 세션 관리.
- `src/generator/`: Gemini API 기반 이미지 분석 및 포스트 생성.
- `src/editor/`: 플랫폼별 에디터(스마트에디터 ONE 등) 인터렉션 로직.
- `data/`: 세션 정보, 입력 이미지, 생성된 포스트 JSON 등 저장.
- `.agent/`: 슬래시 명령어(/blog-automate) 및 AI 에이전트 스킬 정의.

## 📄 라이선스
MIT License
