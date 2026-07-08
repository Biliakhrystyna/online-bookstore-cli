import os

BOOKS_FILE = "books.txt"


def load_books():
    """Читає книги з файлу та повертає список словників."""
    books = []
    if not os.path.exists(BOOKS_FILE):
        return books

    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 5:
                books.append({
                    "author": parts[0],
                    "title": parts[1],
                    "genre": parts[2],
                    "price": float(parts[3]),
                    "stock": int(parts[4])
                })
    return books


def save_books(books):
    """Записує оновлений список книг назад у файл."""
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        for b in books:
            f.write(f"{b['author']}|{b['title']}|{b['genre']}|{b['price']}|{b['stock']}\n")


def display_and_buy_books():
    """Виводить список книг і обробляє логіку покупки."""
    
    
    print_catalog = True 
    
    while True:
        books = load_books()
        if not books:
            print("\n Наразі магазин порожній. Книг немає.")
            return

        if print_catalog:
            print("\n=== Каталог книг ===")
            for i, b in enumerate(books, 1):
                status = f"{b['stock']} шт." if b['stock'] > 0 else "Немає в наявності"
                print(f"{i}. {b['author']} - {b['title']} ({b['genre']}) | {b['price']} грн | Залишок: {status}")
            print("\n0. Повернутися до головного меню")
            
            print_catalog = False 
        
        choice = input("\nВведіть номер книги для покупки (або 0 для виходу): ")
        
        if choice == '0':
            break
            
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(books):
                if books[idx]['stock'] > 0:
                    # Зменшуємо кількість на 1 і зберігаємо у файл
                    books[idx]['stock'] -= 1
                    save_books(books)
                    print(f"\nВи успішно придбали книгу '{books[idx]['title']}'!")
                    
                    # Запитуємо, чи хоче користувач продовжити покупки
                    continue_buying = input("Бажаєте придбати ще книги (y/n)? ").strip().lower()
                    if continue_buying != 'y':
                        break  # Виходимо з циклу покупок і повертаємось в головне меню
                    else:
                        print_catalog = True 
                        
                else:
                    print(f"\n На жаль, книга '{books[idx]['title']}' закінчилася.")
                   
            else:
                print("\nКниги з таким номером не існує. Спробуйте ще раз.")
                
        else:
            print("\nБудь ласка, введіть коректне число.")
            