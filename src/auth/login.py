import os
import json
import asyncio
import time
import random
import pyperclip
import pyautogui
from playwright.async_api import async_playwright, BrowserContext, Page
from playwright_stealth import Stealth


from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class NaverLogin:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.naver_id = os.getenv("NAVER_ID")
        self.naver_pw = os.getenv("NAVER_PW")
        self.session_path = Path("data/sessions/browser_state.json")
        self.browser = None
        
    async def get_context(self, playwright) -> BrowserContext:
        """세션이 저장되어 있으면 불러오고, 없으면 새로 생성하여 반환합니다."""
        # 브라우저 객체를 self에 저장하여 세션 유지 보장
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        if self.session_path.exists():
            print(f"기존 세션을 불러옵니다: {self.session_path}")
            # storage_state를 사용할 때 브라우저 설정(user_agent 등)을 맞추는 것이 좋습니다.
            context = await self.browser.new_context(
                storage_state=str(self.session_path),
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
        else:
            print("새로운 세션을 생성합니다.")
            context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            
        return context

    async def save_session(self, context: BrowserContext):
        """현재 세션 상태를 파일로 저장합니다."""
        self.session_path.parent.mkdir(parents=True, exist_ok=True)
        await context.storage_state(path=str(self.session_path))
        print(f"세션이 저장되었습니다: {self.session_path}")

    async def is_logged_in(self, page: Page) -> bool:
        """현재 페이지에서 로그인 상태인지 확인합니다."""
        try:
            # 네이버 메인에서 로그인 정보가 있는지 확인
            print("로그인 상태를 확인합니다...")
            # Naver 메인은 컨텐츠가 많아 networkidle이 오래 걸릴 수 있으므로 
            # domcontentloaded와 짧은 타임아웃을 사용합니다.
            await page.goto("https://www.naver.com", timeout=15000)
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
            
            # 1. 로그인 링크(nidlogin.login)가 없으면 로그인 된 것으로 간주
            # 2. 프로필 영역(MyView, gnb 등)이 보이면 로그인 된 것
            # 3. 로그아웃 버튼(MY_VIEW, btn_logout 등)이 보이면 확실히 로그인 된 것
            login_link = await page.query_selector("a[href*='nidlogin.login']")
            # MyView 영역은 CSR로 로드될 수 있으므로 약간의 지연 후 체크
            await asyncio.sleep(1) 
            my_info = await page.query_selector(".MyView-module__my_info___fB0l, .gnb_my_name, .gnb_my_interface")
            logout_btn = await page.query_selector("[class*='btn_logout']")
            
            is_logged = login_link is None or my_info is not None or logout_btn is not None
            
            if is_logged:
                print("이미 로그인되어 있는 상태입니다.")
            else:
                print("로그인이 필요한 상태입니다.")
                
            return is_logged
        except Exception as e:
            print(f"로그인 상태 확인 과정 중 (정상적일 수 있는) 타임아웃/오류 발생: {e}")
            # 타임아웃이 나더라도 로그아웃 버튼이 있는지 한 번 더 확인
            try:
                logout_btn = await page.query_selector("[class*='btn_logout']")
                if logout_btn:
                    print("로그아웃 버튼을 발견하여 로그인 상태로 간주합니다.")
                    return True
            except:
                pass
            return False

    async def login_with_stealth(self, page: Page):
        """환경 변수의 값을 직접 타이핑하여 로그인 (지연 시간을 두어 봇 감지 우회)"""
        print("네이버 로그인을 시작합니다.")
        await page.goto("https://nid.naver.com/nidlogin.login")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)
        
        # 브라우저 창 활성화
        await page.bring_to_front()
        
        # ID 입력
        print(f"ID({self.naver_id})를 입력합니다.")
        await page.wait_for_selector("#id")
        await page.click("#id")
        await asyncio.sleep(0.5)
        # 텍스트 입력 전에 입력란을 비웁니다
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type(self.naver_id, delay=random.randint(100, 200)) 
        await asyncio.sleep(0.5)
        
        # PW 입력
        print("PW를 입력합니다.")
        await page.wait_for_selector("#pw")
        await page.click("#pw")
        await asyncio.sleep(0.5)
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type(self.naver_pw, delay=random.randint(100, 200))
        await asyncio.sleep(0.5)
        
        # 로그인 버튼 클릭 (Enter 키 또는 직접 클릭)
        print("로그인 버튼을 클릭합니다.")
        await page.keyboard.press("Enter")
        # await page.click("#log\\.login, .btn_login")
        
        # 로그인 완료 대기 (메인 페이지로 리다이렉트될 때까지)
        print("로그인 완료 대기를 시작합니다 (최대 120초).")
        try:
            # 리다이렉트되는 주요 URL들 감시
            await page.wait_for_url(lambda url: "www.naver.com" in url or "blog.naver.com" in url, timeout=120000)
            print("로그인이 완료되었습니다.")
        except Exception:
            print("로그인 완료 확인 실패 (보안 문자나 추가 인증이 필요할 수 있습니다).")



    async def start(self):
        """로그인 모듈의 메인 실행 프로세스"""
        async with async_playwright() as p:
            context = await self.get_context(p)
            page = await context.new_page()
            await Stealth().apply_stealth_async(page)


            
            if not await self.is_logged_in(page):
                await self.login_with_stealth(page)
                await self.save_session(context)
            else:
                print("이미 로그인되어 있습니다.")
            
            # 테스트를 위해 잠시 대기 후 종료
            await asyncio.sleep(2)
            await context.close()

if __name__ == "__main__":
    login_module = NaverLogin(headless=False)
    asyncio.run(login_module.start())
