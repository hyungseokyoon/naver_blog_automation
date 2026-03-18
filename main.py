import asyncio
import argparse
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from src.auth import NaverLogin
from src.editor import NaverBlogWriter

async def run_naver_list():
    async with async_playwright() as p:
        # 로그인 모듈 초기화
        login_module = NaverLogin(headless=False)
        
        # 브라우저 컨텍스트 및 페이지 생성 (스텔스 적용)
        context = await login_module.get_context(p)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        # 로그인 상태 확인 (목록 조회는 비로그인으로도 가능하지만, 
        # 비공개 글 등을 고려하여 세션 유지 여부만 체크)
        await login_module.is_logged_in(page)
            
        # 블로그 글쓰기 모듈 초기화 (목록 조회 기능 포함)
        writer = NaverBlogWriter(page)
            
        # 목록 조회 실행
        try:
            await writer.get_post_list()
        except Exception as e:
            print(f"Naver 목록 조회 중 오류 발생: {e}")
            
        await context.close()

async def run_naver_automation(title, content):
    async with async_playwright() as p:
        # 로그인 모듈 초기화
        login_module = NaverLogin(headless=False)
        
        # 브라우저 컨텍스트 및 페이지 생성 (스텔스 적용)
        context = await login_module.get_context(p)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        # 로그인 상태 확인 및 필요시 로그인 수행
        if not await login_module.is_logged_in(page):
            await login_module.login_with_stealth(page)
            await login_module.save_session(context)
        else:
            print("이미 로그인되어 있습니다. 세션을 유지합니다.")
            
        # 블로그 글쓰기 모듈 초기화
        writer = NaverBlogWriter(page)
            
        # 포스팅 실행
        try:
            print(f"[Naver] 포스팅을 시작합니다. 제목: {title}")
            await writer.write_test_post(title=title, content=content)
            print("=== 최종 확인: Naver 포스팅이 정상적으로 업로드되었습니다! ===")
        except Exception as e:
            print(f"Naver 포스팅 과정 중 오류 발생: {e}")
            
        # 결과 확인 후 종료 대기
        await asyncio.sleep(5)
        await context.close()

async def run_wordpress_automation(title, content):
    """Wordpress 자동화 (추후 구현 예정)"""
    print(f"[Wordpress] 포스트 작성을 시도합니다 (Placeholder). 제목: {title}")
    print("오류: Wordpress 모듈은 아직 구현되지 않았습니다.")
    await asyncio.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Platform Blog Automation CLI tool")
    parser.add_argument("--write", action="store_true", help="Write a new post")
    parser.add_argument("--list", action="store_true", help="List recent posts")
    parser.add_argument("--platform", type=str, choices=["naver", "wordpress"], default="naver", help="Target blog platform")
    parser.add_argument("--title", type=str, default="test", help="Post title")
    parser.add_argument("--content", type=str, default="test", help="Post content")
    
    args = parser.parse_args()
    
    if args.write:
        if args.platform == "naver":
            asyncio.run(run_naver_automation(args.title, args.content))
        elif args.platform == "wordpress":
            asyncio.run(run_wordpress_automation(args.title, args.content))
    elif args.list:
        if args.platform == "naver":
            asyncio.run(run_naver_list())
        else:
            print(f"오류: {args.platform} 플랫폼은 아직 'list'를 지원하지 않습니다.")
    else:
        parser.print_help()
