---
name: blog-automation
description: "네이버 스마트에디터 ONE을 이용한 블로그 포스팅 자동화 및 브라우저 제어를 담당합니다."
---

# 블로그 자동화 스킬 (Blog Automation)

이 스킬은 네이버 블로그 에디터와 상호작용하기 위한 전문적인 도구와 지침을 제공합니다.

## 주요 기능
- **선택적 인증 (Selective Authentication)**: 로그아웃 버튼(`.btn_logout`) 존재 여부를 확인하여 세션 유효성을 검사하고, 불필요한 로그인을 방지합니다.
- **스텔스 타이핑 (Stealth Typing)**: 클립보드 방식 대신 무작위 지연 시간을 포함한 직접 키보드 입력을 통해 ID/PW 및 본문을 작성하여 봇 탐지를 우회합니다.
- **직접 탐색 (Direct Navigation)**: 중간 목록 페이지를 거치지 않고 글쓰기 URL(`https://blog.naver.com/{blog_id}/postwrite`)로 직접 이동하여 속도와 안정성을 높였습니다.
- **동적 에디터 핸들링 (Dynamic Editor Handling)**: 다중 레이어 CSS 셀렉터와 Tab 키 내비게이션을 활용하여 네이버 스마트에디터 ONE의 제목 및 본문 입력을 자동화합니다.
- **자동 발행 (Auto-Publishing)**: 프레임과 팝업 레이어 전반에서 '발행' 버튼을 찾아 클릭하고 최종 확인 과정을 수행합니다.

## 워크플로우 (CLI 사용법)
`main.py`는 이 스킬의 주요 실행 파일이며, 포스팅 작성 및 목록 조회를 지원합니다:

```bash
# 네이버 - 글 작성
python main.py --write --platform "naver" --title "제목" --content "내용"

# 네이버 - 목록 조회 (최근 10개)
python main.py --list --platform "naver"

# 워드프레스 (기본 구조만 포함)
python main.py --write --platform "wordpress" --title "제목" --content "내용"
```

## 슬래시 명령어 (Slash Commands)
`/blog-automate` 명령어를 통해 이 스킬을 호출할 수 있습니다:
- `/blog-automate write --platform "naver" --title "제목" --content "내용"`
- `/blog-automate list --platform "naver"`
