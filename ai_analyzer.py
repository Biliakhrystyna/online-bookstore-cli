import os
import google.generativeai as genai
from dotenv import load_dotenv
from github_skill import get_file_content


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_repo(owner, repo, file_paths):
  
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    
    full_code_context = ""
    for path in file_paths:
        content = get_file_content(owner, repo, path)
        if content:
            full_code_context += f"\n\n--- FILE: {path} ---\n{content}"
    
   
    prompt = f"""
    Проаналізуй цей репозиторій:
    {full_code_context}
    
    Твоя відповідь має складатися з двох частин, чітко розділених тегом ---SPLIT---:
    
    Частина 1 (JSON): Поверни об'єкт із ключами: language, summary, issues, recommendations.
    
    Частина 2 (Markdown): Напиши професійний звіт:
    - Заголовок 'Code Analysis Report'.
    - Таблиця з аналізом файлів.
    - Детальний опис проблем та їх вирішення.
    """
    
    # 3. Запит до моделі
    response = model.generate_content(prompt)
    return response.text