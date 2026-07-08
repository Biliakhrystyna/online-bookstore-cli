from book_catalog import display_and_buy_books, search_books
from user_manager import register_user, load_users
def display_menu():
    while True:
        print("\n=== Інтернет-книгарня ===")
        print("1. Переглянути наявні книги")
        print("2. Пошук книг")
        print("3. Вхід")
        print("4. Реєстрація")
        print("5. Історія покупок")
        print("0. Вийти з програми")
        
        choice = input("\nОберіть дію (введіть цифру 0-5): ")
        
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
        elif choice == '0':
            print("\nДякуємо, що завітали! До побачення ")
            break  # Вихід із циклу та завершення програми
        else:
            print("\n Невірна команда. Будь ласка, введіть цифру від 0 до 5.")

if __name__ == "__main__":
    display_menu()