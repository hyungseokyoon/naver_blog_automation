---
description: Naver 블로그 포스팅 자동화 명령 인터페이스
---

이 워크플로우는 블로그에 포스팅을 작성하거나 목록을 조회하는 기능을 수행합니다.

# 사용 방법
- **글 작성**: `/blog-automate write --platform "naver" --title "제목" --content "내용"`
- **목록 조회**: `/blog-automate list --platform "naver"`

(platform은 naver, wordpress 중 선택 가능하며 기본값은 naver입니다. 현재 wordpress는 write 플레이스홀더만 존재합니다.)

// turbo
1. 다음 명령어를 실행하여 동작을 수행합니다:
`python main.py --{{command}} --platform "{{platform}}" --title "{{title}}" --content "{{content}}"`
