# Naver Blog Automation

An automated tool for creating and publishing high-quality blog posts on Naver.com using AI content generation and stealthy browser automation.

## 🚀 Overview
This project automates the Naver blog posting process, from generating rich content using Gemini AI to handling complex browser interactions with Naver's Smart Editor One.

## ✨ Key Features
- **AI Content Generation**: Leverages Google Gemini 2.0 Flash for SEO-optimized content creation.
- **Stealth Automation**: Uses Playwright with clipboard-based login to bypass bot detection mechanisms.
- **Bulk Processing**: Supports automated posting from Excel-based data sources.
- **Modern Editor Support**: Specifically designed for Naver's Smart Editor One (Block Editor).

## 🛠 Tech Stack
- **Python**: Core logic and automation scripts.
- **Playwright**: Modern browser automation engine.
- **Google Generative AI**: Gemini API for content generation.
- **BeautifulSoup4**: Content parsing and transformation.
- **Openpyxl**: Excel data management for bulk tasks.

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/hyungseokyoon/naver_blog_automation.git
   cd naver_blog_automation
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
4. Set up environment variables in a `.env` file:
   ```env
   NAVER_ID=your_id
   NAVER_PW=your_password
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 📂 Project Structure
- `src/auth/`: Login and session management.
- `src/ai/`: Gemini-powered content generation.
- `src/editor/`: Smart Editor One interaction logic.
- `src/parser/`: Data input and content mapping.
- `src/utils/`: Helper utilities for logging and images.
- `data/`: Inputs, logs, and browser sessions.

## 📄 License
MIT License
