import os

USERS_FILE = "users.txt"

def load_users():
    """Читає користувачів з файлу та повертає словник {username: дані_користувача}."""
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
        
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
           
            if len(parts) >= 2:
                # Зберігаємо всі дані у вигляді внутрішнього словника
                users[parts[0]] = {
                    "password": parts[1],
                    "first_name": parts[2] if len(parts) > 2 else "",
                    "last_name": parts[3] if len(parts) > 3 else "",
                    "dob": parts[4] if len(parts) > 4 else ""
                }
    return users

def save_user(username, password, first_name, last_name, dob):
    """Додає нового користувача у файл (логін|пароль|ім'я|прізвище|дата)."""
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}|{password}|{first_name}|{last_name}|{dob}\n")

def register_user():
    """Модуль інтерактивної реєстрації нового користувача."""
    print("\n=== Реєстрація нового користувача ===")
    
    users = load_users()
    
    while True:
        first_name = input("Введіть ваше ім'я: ").strip().capitalize()
        if not first_name or "|" in first_name:
            print(" Ім'я не може бути порожнім або містити '|'.")
            continue
        break
    
    while True:
        last_name = input("Введіть ваше прізвище: ").strip().capitalize()
        if not last_name or "|" in last_name:
            print("Прізвище не може бути порожнім або містити '|'.")
            continue
        break
    
    while True:
        dob = input("Введіть дату народження (наприклад, 15.05.2003): ").strip()
        if not dob or "|" in dob:
            print(" Дата народження не може бути порожньою або містити '|'.")
            continue
        break
        
    while True:
        username = input("Введіть логін користувача  ").strip()
        
            
        if not username:
            print("Логін користувача не може бути порожнім.")
            continue
            
        if username in users:
            print("Користувач з таким логіном вже існує! Спробуйте інше.")
            continue
            
            
        break 
        
  
    while True:
        password = input("Введіть пароль: ").strip()
        
        if len(password) < 4:
            print("Пароль занадто короткий. Мінімум 4 символи.")
            continue
            
        if "|" in password:
            print("Пароль не може містити символ '|'.")
            continue
            
        break
   
    # Зберігаємо всі валідні дані
    save_user(username, password, first_name, last_name, dob)
    print(f"\nВітаємо, {first_name} {last_name}! Ви успішно зареєструвалися.")