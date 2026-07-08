import os
from datetime import datetime

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
   

    save_user(username, password, first_name, last_name, dob)
    print(f"\nВітаємо, {first_name} {last_name}! Ви успішно зареєструвалися.")

def login_user():
   
    print("\n=== Вхід у систему ===")
    
    users = load_users()
    
    if not users:
        register_user()
        return None

    while True:
        username = input("Введіть логін ").strip()
        
            
        # Якщо логін не знайдено в базі
        if username not in users:
            print("\n Користувача з таким логіном не знайдено.")
            redirect = input("Бажаєте зареєструватися прямо зараз (y/n)? ").strip().lower()
            
            if redirect == 'y':
                register_user()
                return None 
            else:
                continue 
                
        
        while True:
            password = input("Введіть пароль (або '0' для відміни): ").strip()
            
            if password == '0':
                return None
                
            if users[username]["password"] == password:
                first_name = users[username].get("first_name", username)
                print(f"\nУспішний вхід! З поверненням, {first_name}!")
                return username 
            else:
                print(" Невірний пароль. Спробуйте ще раз.")

HISTORY_FILE = "history.txt"

def record_purchase(username, book_title, price):
    """Записує факт покупки у файл історії."""
    # Отримуємо поточну дату та час
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}|{book_title}|{price}|{date_str}\n")

def view_purchase_history(username):
   
    print(f"\n=== Історія покупок ({username}) ===")
    
    if not os.path.exists(HISTORY_FILE):
        print(" Ваша історія покупок порожня.")
        return

    found = False
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            # Перевіряємо, чи є 4 елементи і чи збігається логін
            if len(parts) == 4 and parts[0] == username:
                print(f"- {parts[1]} ({parts[2]} грн) | Куплено: {parts[3]}")
                found = True

    if not found:
        print("Ваша історія покупок порожня.")