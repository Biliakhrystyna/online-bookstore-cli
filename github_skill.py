import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

def get_repo_structure(owner, repo, branch="main"):
    """Отримує список усіх файлів репозиторію через GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get("tree", [])
    else:
        print(f"Помилка API: {response.status_code}")
        return []

def get_file_content(owner, repo, file_path):
    """Отримує вміст конкретного файлу."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        content_base64 = response.json().get("content", "")
        
        return base64.b64decode(content_base64).decode("utf-8")
    return None