from book_catalog import display_and_buy_books, search_books
from user_manager import register_user, load_users
from github_skill import get_repo_structure, get_file_content

# Константи репозиторію за замовчуванням
OWNER = "Biliakhrystyna"
REPO = "online-bookstore-cli" 

def show_github_structure():
    """Виводить структуру всього репозиторію."""
    print(f"\n--- Структура репозиторію {OWNER}/{REPO} ---")
    files = get_repo_structure(OWNER, REPO)
    if files:
        for item in files:
            print(f"[{item['type'].upper()}]: {item['path']}")
    else:
        print("Не вдалося завантажити структуру репозиторію.")

def view_any_github_file():
    """Дозволяє користувачеві прочитати БУДЬ-ЯКИЙ файл з репозиторію."""
    file_path = input("\nВведіть повний шлях до файлу в репозиторії (наприклад, main.py або README.md): ").strip()
    if not file_path:
        print("Шлях до файлу не може бути порожнім.")
        return

    content = get_file_content(OWNER, REPO, file_path)
    if content:
        print(f"\n--- Вміст файлу: {file_path} (перші 500 символів) ---")
        print(content[:500])
        print("--------------------------------------------------")
    else:
        print(f"Файл '{file_path}' не знайдено або виникла помилка доступу.")

def display_menu():
    while True:
        print("\n=== Інтернет-книгарня ===")
        print("1. Переглянути наявні книги")
        print("2. Пошук книг")
        print("3. Вхід")
        print("4. Реєстрація")
        print("5. Історія покупок")
        print("6. [GitHub] Переглянути структуру репозиторію")
        print("7. [GitHub] Прочитати вміст будь-якого файлу")
        print("0. Вийти з програми")
        
        choice = input("\nОберіть дію (введіть цифру 0-7): ")
        
        if choice == '1':
            display_and_buy_books()
        elif choice == '2':
            search_books()
        elif choice == '3':
            load_users()
        elif choice == '4':
            register_user()
        elif choice == '5':
            print("\n[В розробці] Ваша історія покупок...")
        elif choice == '6':
            show_github_structure()
        elif choice == '7':
            view_any_github_file()
        elif choice == '0':
            print("\nДякуємо, що завітали! До побачення 👋")
            break
        else:
            print("\n❌ Невірна команда. Будь ласка, введіть цифру від 0 до 7.")

if __name__ == "__main__":
    display_menu()