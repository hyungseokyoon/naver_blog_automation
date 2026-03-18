import os
import json
import asyncio
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

class GeminiGenerator:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")
        
        # New Google GenAI SDK Client
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash" 
        
    async def generate_post(self, platform, folder_path):
        """지정된 폴더의 이미지를 분석하여 블로그 포스팅 내용을 생성합니다."""
        folder = Path(folder_path)
        if not folder.exists():
            print(f"오류: 폴더를 찾을 수 없습니다: {folder_path}")
            return None

        # 이미지 파일들 찾기
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = sorted([f for f in folder.iterdir() if f.suffix.lower() in image_extensions])
        
        if not image_files:
            print("이미지가 없습니다. 텍스트로만 포스팅을 생성합니다.")
            contents = ["이미지 없이 블로그 포스트를 작성해줘."]
        else:
            print(f"{len(image_files)}개의 이미지를 분석 중...")
            contents = []
            for img_path in image_files:
                # Pillow를 사용하거나 직접 바이트로 전달 가능
                # SDK는 경로를 직접 처리하거나 바이트를 처리함
                with open(img_path, 'rb') as f:
                    image_data = f.read()
                contents.append(types.Part.from_bytes(data=image_data, mime_type=f"image/{img_path.suffix[1:] if img_path.suffix != '.jpg' else 'jpeg'}"))
            
            contents.append(f"이 {len(image_files)}개의 사진들을 순서대로 분석해서 {platform} 블로그 포스트를 작성해줘.")

        # 플랫폼별 프롬프트 추가
        prompt_text = ""
        if platform == "naver":
            prompt_text = """
            네이버 블로그(Naver Blog)용 포스팅을 작성해줘. 
            친근한 '~해요', '~입니다'체로 작성하고, 실용적인 정보와 개인적인 감상을 섞어줘.
            JSON 형식으로만 응답해줘:
            {
              "title": "제목",
              "content": [
                {"type": "text", "value": "설명"},
                {"type": "image", "file": "파일명 (분석한 이미지 중 하나)", "caption": "설명"},
                ...
              ],
              "tags": ["태그1", "태그2"]
            }
            이미지 파일명은 내가 준 파일들의 순서를 고려해서 매칭해줘.
            """
        else:
            prompt_text = f"{platform} 블로그용 JSON 데이터를 생성해줘."

        contents.append(prompt_text)

        # AI 생성 실행
        try:
            loop = asyncio.get_event_loop()
            # New SDK sync call wrapped in executor
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
            )
            
            res_json = response.parsed if hasattr(response, 'parsed') else json.loads(response.text)
            
            # 파일로 저장
            output_file = folder / "post.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(res_json, f, ensure_ascii=False, indent=2)
            
            print(f"성공: {output_file} 생성 완료")
            return res_json
        except Exception as e:
            print(f"Gemini API 호출 중 오류 발생: {e}")
            return None
