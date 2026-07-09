import os
import json
import requests
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

def run_full_analysis(owner, repo, branch="main"):
    github_token = os.getenv("GITHUB_TOKEN")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not github_token or not gemini_key:
        print("Помилка: Відсутні необхідні API ключі в .env файлі!")
        return

    # 1. Отримання структури через GitHub API
    print(f"Зчитування структури репозиторію {owner}/{repo}...")
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Помилка GitHub API: {res.status_code}")
        return
        
    tree = res.json().get("tree", [])
    file_list = [item["path"] for item in tree if item["type"] == "blob"]
    repo_structure_text = "\n".join(file_list)

    # Виводимо структуру файлів у консоль
    print("\n Знайдена структура файлів репозиторію:")
    print("-" * 50)
    for file_path in file_list:
        print(f"   {file_path}")
    print("-" * 50 + "\n")

 
    print("Надсилання структури на аналіз до Gemini LLM...")
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={gemini_key}"
    
    prompt = (
        "Analyze the following repository structure and return a JSON object with keys: "
        "'primary_language', 'potential_issues' (list), 'solutions' (list), 'comments' (string). "
        "Return ONLY pure JSON code without any markdown block formatting.\n\n"
        f"Repository files:\n{repo_structure_text}"
    )
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    gemini_res = requests.post(gemini_url, json=payload)
    if gemini_res.status_code != 200:
        print(f"Помилка Gemini API: {gemini_res.status_code}\n{gemini_res.text}")
        return

    try:
        raw_response = gemini_res.json()["candidates"][0]["content"]["parts"][0]["text"]
        analysis_data = json.loads(raw_response)
    except Exception as e:
        print(f"Не вдалося розпарсити відповідь від AI: {e}")
        print(f"Сира відповідь сервера: {gemini_res.text}")
        return

    # 3. Збереження результатів у директорію /output
    os.makedirs("output", exist_ok=True)
    
    # Запис у analysis.json
    with open("output/analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=4)
        
    # Запис у report.md
    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write(f"# Аналітичний звіт репозиторію {owner}/{repo}\n\n")
        f.write(f"**Основна мова проєкту:** {analysis_data.get('primary_language', 'Не визначено')}\n\n")
        f.write("##  Виявлені проблеми\n")
        for issue in analysis_data.get("potential_issues", []):
            f.write(f"- {issue}\n")
        f.write("\n##  Рекомендовані рішення\n")
        for solution in analysis_data.get("solutions", []):
            f.write(f"- {solution}\n")
        f.write(f"\n## Загальні коментарі\n{analysis_data.get('comments', '')}\n")

    print("Аналіз успішно завершено! Файли збережено в директорію /output")

if __name__ == "__main__":
    
    run_full_analysis("Biliakhrystyna", "online-bookstore-cli")