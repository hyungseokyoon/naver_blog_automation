---
description: Naver/WordPress 블로그 자동화 명령 (목록 조회, AI 생성, 발행)
---

# 블로그 자동화 워크플로우

1. 실행할 명령어를 선택하고 필요한 옵션을 입력하세요:
- **list**: 블로그 목록 조회 (`--platform naver`)
- **generate**: AI 글 생성 (`--platform naver --folder [폴더명]`)
- **write**: 실제 발행 (`--platform naver --folder [폴더명]` 또는 `--title "제목" --content "내용"`)

// turbo
2. 다음 명령어를 실행하여 파이썬 스크립트를 구동합니다:
`python main.py --{{command}} --platform "{{platform}}" {{#if folder}}--folder "{{folder}}"{{/if}}{{#if title}} --title "{{title}}"{{/if}}{{#if content}} --content "{{content}}"{{/if}}`
