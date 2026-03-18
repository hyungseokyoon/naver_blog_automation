import asyncio
import argparse
import os
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from src.auth import NaverLogin
from src.editor import NaverBlogWriter
from src.generator.gemini_generator import GeminiGenerator

async def run_naver_list():
    async with async_playwright() as p:
        login_module = NaverLogin(headless=False)
        context = await login_module.get_context(p)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        await login_module.is_logged_in(page)
        writer = NaverBlogWriter(page)
        try:
            await writer.get_post_list()
        except Exception as e:
            print(f"Naver 목록 조회 중 오류 발생: {e}")
        await context.close()

async def run_generate(platform, folder_name):
    """AI를 이용해 포스팅 내용을 폴더 내 이미지 기반으로 생성합니다."""
    # 폴더 경로 구성 (data/inputs/{platform}/{folder_name})
    base_dir = os.path.join("data", "inputs", platform)
    folder_path = os.path.join(base_dir, folder_name)
    
    if not os.path.exists(folder_path):
        print(f"오류: 폴더를 찾을 수 없습니다: {folder_path}")
        return

    generator = GeminiGenerator()
    await generator.generate_post(platform, folder_path)

async def run_naver_automation(title, content, folder_name=None):
    async with async_playwright() as p:
        login_module = NaverLogin(headless=False)
        context = await login_module.get_context(p)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        if not await login_module.is_logged_in(page):
            await login_module.login_with_stealth(page)
            await login_module.save_session(context)
            
        writer = NaverBlogWriter(page)
        
        try:
            if folder_name:
                # 폴더 내 post.json 읽어서 포스팅
                folder_path = os.path.join("data", "inputs", "naver", folder_name)
                post_json_path = os.path.join(folder_path, "post.json")
                
                if not os.path.exists(post_json_path):
                    print(f"오류: {post_json_path} 파일이 없습니다. 먼저 --generate를 실행하세요.")
                    return

                with open(post_json_path, "r", encoding="utf-8") as f:
                    post_data = json.load(f)
                
                print(f"[Naver] 폴더 데이터를 기반으로 포스팅을 시작합니다: {folder_name}")
                await writer.write_post_from_json(post_data, folder_path)
            else:
                # 일반 텍스트 포스팅 (테스트용)
                print(f"[Naver] 텍스트 포스팅을 시작합니다. 제목: {title}")
                await writer.write_test_post(title=title, content=content)
                
            print("=== Naver 포스팅 완료! ===")
        except Exception as e:
            print(f"Naver 포스팅 중 오류 발생: {e}")
            
        await asyncio.sleep(3)
        await context.close()

async def run_wordpress_automation(title, content, folder_name=None):
    print(f"[Wordpress] 포스트 작성을 시도합니다 (Placeholder).")
    print("오류: Wordpress 모듈은 아직 구현되지 않았습니다.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Platform Blog Automation CLI tool")
    parser.add_argument("--write", action="store_true", help="Write a new post")
    parser.add_argument("--list", action="store_true", help="List recent posts")
    parser.add_argument("--generate", action="store_true", help="Generate post content using AI")
    parser.add_argument("--platform", type=str, choices=["naver", "wordpress"], default="naver", help="Target blog platform")
    parser.add_argument("--folder", type=str, help="Folder name in data/inputs/{platform}/")
    parser.add_argument("--title", type=str, default="test", help="Post title (for direct write)")
    parser.add_argument("--content", type=str, default="test", help="Post content (for direct write)")
    
    args = parser.parse_args()
    
    if args.generate:
        if not args.folder:
            print("오류: --generate 사용 시 --folder 인자가 필요합니다.")
        else:
            asyncio.run(run_generate(args.platform, args.folder))
    elif args.write:
        if args.platform == "naver":
            asyncio.run(run_naver_automation(args.title, args.content, args.folder))
        elif args.platform == "wordpress":
            asyncio.run(run_wordpress_automation(args.title, args.content, args.folder))
    elif args.list:
        if args.platform == "naver":
            asyncio.run(run_naver_list())
        else:
            print(f"오류: {args.platform} 플랫폼은 아직 'list'를 지원하지 않습니다.")
    else:
        parser.print_help()
