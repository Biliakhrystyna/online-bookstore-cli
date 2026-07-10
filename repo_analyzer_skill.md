---
id: repo_codebase_analyzer
name: Repository Structure and AI Analyzer
description: Скіл для завантаження дерева файлів репозиторію через GitHub API та його експертного аналізу за допомогою Gemini API.
version: 1.0.0
inputs:
  - name: GITHUB_TOKEN
    type: string
    required: true
    description: Персональний токен доступу GitHub
  - name: GEMINI_API_KEY
    type: string
    required: true
    description: Ключ доступу до Gemini API
  - name: REPO_OWNER
    type: string
    required: true
    description: Власник репозиторію (Username)
  - name: REPO_NAME
    type: string
    required: true
    description: Назва репозиторію
  - name: REPO_BRANCH
    type: string
    required: false
    default: main
    description: Гілка репозиторію
outputs:
  - path: output/analysis.json
    type: json
    description: Повний структурований звіт від LLM у форматі JSON
  - path: output/report.md
    type: markdown
    description: Читабельний аналітичний звіт для розробників
---

# Інструкція виконання вміння (Skill Execution Flow)

Цей скіл автоматизує аудит кодової бази, виявляючи потенційні архітектурні проблеми, мову проєкту та надаючи рекомендації щодо покращення.

## Етапи виконання

1. **Ініціалізація та валідація:** Скрипт перевіряє наявність токенів `GITHUB_TOKEN` та `GEMINI_API_KEY` в системному оточенні або файлі `.env`.
2. **Збір метаданих репозиторію:** За допомогою GitHub Trees API виконується рекурсивний запит для отримання повного списку файлів проєкту.
3. **Формування запиту до LLM:** Отриманий список файлів передається у структурований промпт для моделі Gemini.
4. **Генерація артефактів:**
   - Отримана відповідь валідується як JSON.
   - Створюється директорія `output/`.
   - Записуються результати в `analysis.json` та конвертуються у зручний `report.md`.

## Скрипт реалізації (analyzer.py)

Для запуску цього вміння використовується наступний Python код:

```python
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def run_full_analysis(owner, repo, branch="main"):
    github_token = os.getenv("GITHUB_TOKEN")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not github_token or not gemini_key:
        print("Помилка: Відсутні необхідні API ключі в .env файлі!")
        return

    # 1. Отримання структури через GitHub API
    print(f" Зчитування структури репозиторію {owner}/{repo}...")
    url = f"[https://api.github.com/repos/](https://api.github.com/repos/){owner}/{repo}/git/trees/{branch}?recursive=1"
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

    # 2. Запит до Gemini API
    print(" Надсилання структури на аналіз до Gemini LLM...")
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={gemini_key}"
    
    prompt = f"Analyze the following repository structure and return a JSON object with keys: 'primary_language', 'potential_issues' (list), 'solutions' (list), 'comments' (string). Return ONLY pure JSON code.\n\nRepository files:\n{repo_structure_text}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    gemini_res = requests.post(gemini_url, json=payload)
    if gemini_res.status_code != 200:
        print(f"Помилка Gemini API: {gemini_res.status_code}")
        return

    try:
        raw_response = gemini_res.json()["candidates"][0]["content"]["parts"][0]["text"]
        analysis_data = json.loads(raw_response)
    except Exception as e:
        print(f"Не вдалося розпарсити відповідь від AI: {e}")
        return

    # 3. Збереження результатів у /output
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
        f.write(f"\n##  Загальні коментарі\n{analysis_data.get('comments', '')}\n")

    print(" Аналіз успішно завершено! Файли збережено в директорію /output")

if __name__ == "__main__":
    # Тестовий запуск для твого проєкту
    run_full_analysis("Biliakhrystyna", "online-bookstore-cli")