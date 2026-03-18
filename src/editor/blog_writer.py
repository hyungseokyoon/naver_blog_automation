import asyncio
import os
import random
from playwright.async_api import Page, BrowserContext
from playwright_stealth import Stealth

class NaverBlogWriter:
    def __init__(self, page: Page):
        self.page = page
        self.naver_id = os.getenv("NAVER_ID")
        self.blog_id = os.getenv("NAVER_BLOG_ID") or self.naver_id
        self.frame = None

    async def navigate_to_postwrite(self):
        """블로그 글쓰기 페이지로 직접 이동합니다."""
        # directAccess=true 를 포함한 다이렉트 URL 사용
        url = f"https://blog.naver.com/{self.blog_id}/postwrite"
        print(f"블로그 에디터로 직접 이동합니다: {url}")
        await self.page.goto(url)
        await self.page.wait_for_load_state("networkidle")
        await asyncio.sleep(5) # 에디터 로딩을 위해 충분히 대기

        # mainFrame 로딩 대기 (최대 15초)
        print("에디터 프레임(mainFrame)을 기다리는 중...")
        for _ in range(15):
            frames = self.page.frames
            for f in frames:
                if "mainFrame" in f.name:
                    print(f"mainFrame을 발견했습니다 (URL: {f.url[:50]}...)")
                    self.frame = f
                    break
            if self.frame:
                # 에디터 내부의 특정 요소가 보일 때까지 대기
                try:
                    await self.frame.wait_for_selector(".se-documentTitle, .se-title-text, div[data-placeholder*='제목']", timeout=5000)
                    print("에디터 요소가 프레임 내에 로드되었습니다.")
                    break
                except:
                    pass
            await asyncio.sleep(1)
        
        if not self.frame:
            self.frame = self.page
            print("최종적으로 메인 프레임을 사용합니다.")

    async def handle_popups(self):
        """임시 저장글 복구 및 도움말 팝업을 처리합니다."""
        print("팝업 확인 중...")
        # 1. 도움말 닫기 및 임시 저장글 취소
        popup_selectors = [
            ".se-help-panel-close-button",
            ".se-help-popup-close-button",
            ".btn_close",
            ".se-popup-button-cancel", # 임시 저장글 취소 버튼
            ".se-popup-window .se-section-button:has-text('취소')",
            ".se-popup-button-close"
        ]
        
        for sel in popup_selectors:
            try:
                # frame 내부와 top level(page) 양쪽에서 탐색
                btn = await self.frame.query_selector(sel) or await self.page.query_selector(sel)
                if btn:
                    print(f"발견된 팝업 요소({sel})를 닫습니다.")
                    await btn.click()
                    await asyncio.sleep(1)
            except:
                pass

    async def write_title(self, title: str):
        """제목을 입력합니다."""
        print(f"제목 입력 중: {title}")
        # 제목 영역 클릭 시도
        success = False
        # se-title-area, .se-documentTitle .se-placeholder, .se-placeholder.__title
        selectors = [
            ".se-documentTitle .se-placeholder",
            "div[data-placeholder*='제목']",
            ".se-title-text",
            ".se-placeholder.__title"
        ]
        
        for sel in selectors:
            try:
                el = await self.frame.wait_for_selector(sel, timeout=3000)
                if el:
                    await el.click()
                    success = True
                    break
            except:
                continue
        
        if not success:
            print("제목 셀렉터 탐색 실패. Tab 키로 포커스 이동을 시도합니다.")
            await self.page.keyboard.press("Tab")
            await asyncio.sleep(0.5)

        # 텍스트 입력을 위해 약간의 딜레이
        await self.page.keyboard.type(title, delay=100)
        await asyncio.sleep(1)

    async def write_content(self, content: str):
        """본문을 입력합니다."""
        print(f"본문 입력 중: {content}")
        # 본문 영역 클릭 시도
        success = False
        selectors = [
            "div[data-placeholder*='내용']",
            ".se-content .se-placeholder",
            ".se-component-text",
            ".se-editable"
        ]
        
        for sel in selectors:
            try:
                el = await self.frame.wait_for_selector(sel, timeout=3000)
                if el:
                    await el.click()
                    success = True
                    break
            except:
                continue

        if not success:
            print("본문 셀렉터 탐색 실패. Tab 키로 이동합니다.")
            await self.page.keyboard.press("Tab")
            await asyncio.sleep(0.5)

        await self.page.keyboard.type(content, delay=100)
        await asyncio.sleep(1)

    async def publish(self) -> bool:
        """발행 버튼을 누르고 최종 등록합니다."""
        print("발행 프로세스를 시작합니다.")
        
        # 발행 버튼 셀렉터 (다양한 버전 대응)
        # 발행 버튼은 보통 top menu bar(iframe 안이 아님)에 있는 경우가 많으나 
        # 에디터 버전에 따라 다를 수 있으므로 양쪽 확인
        publish_btn_selectors = [
            "button[class*='publish_btn']",
            ".btn_publish",
            "button:has-text('발행')",
            ".se-publish-button"
        ]
        
        publish_btn = None
        for sel in publish_btn_selectors:
            # top level 우선, 그 다음 frame
            publish_btn = await self.page.query_selector(sel) or await self.frame.query_selector(sel)
            if publish_btn:
                # 보이는지 확인
                try:
                    if await publish_btn.is_visible():
                        break
                except:
                    pass
        
        if not publish_btn:
            print("발행 버튼을 찾을 수 없습니다. 좌표 클릭을 시도합니다.")
            # 보통 우측 상단에 위치. 창 크기에 따라 다를 수 있으므로 90% 지점
            viewport = self.page.viewport_size
            if viewport:
                await self.page.mouse.click(viewport['width'] - 100, 40)
            else:
                await self.page.mouse.click(1000, 40) 
            await asyncio.sleep(2)
        else:
            await publish_btn.click()
            await asyncio.sleep(2)

        # 최종 등록 버튼 (팝업 레이어 - 보통 top window에 생김)
        confirm_btn_selectors = [
            "button[class*='confirm_btn']",
            ".btn_confirm",
            "button:has-text('발행')", # 팝업 내 버튼도 텍스트가 '발행'인 경우 있음
            "button[class*='confirm']",
            ".publish_btn_confirm"
        ]
        
        confirm_btn = None
        for sel in confirm_btn_selectors:
            confirm_btn = await self.page.query_selector(sel) or await self.frame.query_selector(sel)
            if confirm_btn:
                try:
                    if await confirm_btn.is_visible():
                        break
                except:
                    pass
        
        if confirm_btn:
            await confirm_btn.click()
            print("최종 발행 버튼을 클릭했습니다. 업로드 완료 대기 중...")
            try:
                # 로드 성공 시 logNo가 URL에 포함되거나 main.naver로 이동됨
                await self.page.wait_for_url(lambda u: "logNo" in u or "PostView.naver" in u, timeout=60000)
                print("포스팅 업로드 성공 확인!")
                return True
            except:
                print("업로드 완료 URL 리디렉션을 감지하지 못했습니다.")
                return True # 이동은 실패했어도 실제 업로드는 됐을 수 있음
        else:
            print("최종 확인 버튼을 찾지 못했습니다.")
            # 가끔 엔터 키로 발행이 가능한 경우도 있음
            await self.page.keyboard.press("Enter")
            await asyncio.sleep(2)
            return True # 가능성을 열어둠

    async def get_post_list(self):
        """블로그의 포스팅 목록을 가져와 출력합니다."""
        # 블로그 목록 페이지로 이동
        url = f"https://blog.naver.com/PostList.naver?blogId={self.blog_id}"
        print(f"블로그 목록 페이지로 이동합니다: {url}")
        await self.page.goto(url)
        await self.page.wait_for_load_state("networkidle")
        
        # 프레임 찾기
        frame = None
        for f in self.page.frames:
            if "mainFrame" in f.name:
                frame = f
                break
        
        if not frame:
            frame = self.page

        print("포스팅 목록을 분석 중...")
        try:
            # 글 목록이 로드될 때까지 대기
            await frame.wait_for_selector(".post-list, .blog2_container, #postListBody", timeout=10000)
            
            # 포스트 요소들 추출 (제목과 날짜)
            # Naver 블로그의 다양한 템플릿 대응을 위해 여러 셀렉터 시도
            posts = await frame.evaluate("""() => {
                const items = [];
                // 앨범형, 목록형 등 다양한 구조 대응
                const titleElements = document.querySelectorAll('.item_title, .p_title, .tit, .post-title, .title_text');
                const dateElements = document.querySelectorAll('.item_date, .p_date, .date, .post-date, .publish_date');
                
                for (let i = 0; i < titleElements.length; i++) {
                    const title = titleElements[i].innerText.trim();
                    const date = dateElements[i] ? dateElements[i].innerText.trim() : "날짜 없음";
                    if (title) {
                        items.push({ title, date });
                    }
                }
                return items;
            }""")
            
            if not posts:
                print("포스팅을 찾을 수 없습니다.")
                return

            print(f"\n=== {self.blog_id} 블로그 포스팅 목록 (최신순) ===")
            for i, post in enumerate(posts[:10], 1): # 최근 10개만 출력
                print(f"{i}. [{post['date']}] {post['title']}")
            print("==========================================\n")
            
        except Exception as e:
            print(f"목록 추출 중 오류 발생: {e}")

    async def write_test_post(self, title: str = "test", content: str = "test"):
        """테스트 포스팅 전체 과정을 수행합니다."""
        await self.navigate_to_postwrite()
        await self.handle_popups()
        await self.write_title(title)
        await self.write_content(content)
        success = await self.publish()
        if not success:
            raise Exception("발행 과정 중 문제가 발생했습니다.")

