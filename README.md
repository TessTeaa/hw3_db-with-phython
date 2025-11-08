# hw3_db-with-phython
task:
В Python + SQLite виконати наступне:
1) створити базу даних з Д/З-1
2) наповнити базу даними (INSERT ... VALUES ...)
3) виконати SELECT запити з Д/З-2 (або інші) і переконатись, що вони
3.1) коректно відпрацьовують (не повертають помилок)
3.2) вертають очікуваний результат (print ()
результат виконання SQL запиту, таблиця, набір записів)
4*) оновити записи
UPDATE ... SET ... WHERE ...
5*) виконати ті самі запити й перевірити, що результати SELECT (п.3) зміняться відповідно
6*) повний код розв'язку викласти на GitHub (або аналогічний репозиторій) і прикласти лінк на рішення, або ж код рішення, python_solution.py

Документація до програми (Python + SQLite)
Мета роботи

Метою роботи було створення бази даних у SQLite, заповнення її тестовими даними, виконання SELECT та UPDATE запитів, перевірка їх коректності та відображення результатів у Python. Усі операції виконуються програмно через бібліотеку sqlite3.

**Опис функціоналу програми**

Програма реалізована мовою Python і використовує базу даних library.db. Вона складається з кількох логічних блоків: створення бази даних, створення таблиць, додавання даних, виконання SQL-запитів і оновлення записів.

1. Підключення до бази даних
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f" Connected to SQLite DB: {db_file}")
    except Error as e:
        print(f" DB connection error: {e}")
    return conn


**Функція створює або відкриває файл бази даних. Якщо база ще не існує, SQLite автоматично створює її.**

2. Створення таблиць (CREATE TABLE)
def create_tables(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS Loan;
    DROP TABLE IF EXISTS Reader;
    DROP TABLE IF EXISTS Librarian;
    DROP TABLE IF EXISTS Book;
    DROP TABLE IF EXISTS Library;

    CREATE TABLE Library ( ... );
    CREATE TABLE Librarian ( ... );
    CREATE TABLE Reader ( ... );
    CREATE TABLE Book ( ... );
    CREATE TABLE Loan ( ... );
    """)


**Використовується executescript(), що дозволяє запускати кілька SQL операторів одночасно.**

Таблиці моделюють структуру бібліотеки:

Library — бібліотеки
Librarian — бібліотекарі
Reader — читачі
Book — книги
Loan — видача книг

**Встановлені зовнішні ключі (FOREIGN KEY), що забезпечують зв'язки між таблицями.**

3. Додавання даних (INSERT INTO)
def insert_data(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    INSERT INTO Library (...)
    INSERT INTO Librarian (...)
    INSERT INTO Reader (...)
    INSERT INTO Book (...)
    INSERT INTO Loan (...)
    """)


**Після записів викликається conn.commit(), що зберігає зміни у базі.**

4. SELECT запити
def run_select_queries(conn):
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT Book.title, Reader.name, Loan.loan_date
        FROM Loan
        JOIN Book ON Loan.book_id = Book.id
        JOIN Reader ON Loan.reader_id = Reader.id;
    """).fetchall()


**У програмі виконується три вибірки:**

список книг із читачами, які їх взяли (JOIN), список усіх читачів, список бібліотекарів.

**Результати виводяться через print(), що демонструє коректність виконання.**

5. UPDATE — оновлення записів
def update_query(conn):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Loan
        SET status = 'returned'
        WHERE id = 1;
    """)
    conn.commit()


**Після UPDATE повторно виконується SELECT, щоб підтвердити зміну статусу:**

SELECT * FROM Loan;

6. Основна програма
if __name__ == "__main__":
    conn = create_connection("library.db")
    create_tables(conn)
    insert_data(conn)
    run_select_queries(conn)
    update_query(conn)
    conn.close()


Цей блок: створює базу даних, створює таблиці, заповнює даними, виконує SELECT запити, оновлює дані, закриває з’єднання.


Консольний вивід (приклад):

Connected to SQLite DB: library.db
Tables created successfully!
Initial data inserted!

SELECT: Список книг з їхніми читачами
[('1984', 'Taisiia', '2024-12-01')]

UPDATE: повернули книгу
[(1, 1, 1, 1, '2024-12-01', '2024-12-15', 'returned')]
