import sqlite3
from sqlite3 import Error

# ---------------------------- DB CONNECTION ----------------------------

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f" Connected to SQLite DB: {db_file}")
    except Error as e:
        print(f" DB connection error: {e}")
    return conn


# ---------------------------- CREATE TABLES ----------------------------

def create_tables(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS Loan;
    DROP TABLE IF EXISTS Reader;
    DROP TABLE IF EXISTS Librarian;
    DROP TABLE IF EXISTS Book;
    DROP TABLE IF EXISTS Library;

    CREATE TABLE Library (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        type TEXT,
        phone TEXT
    );

    CREATE TABLE Librarian (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT,
        position TEXT,
        hire_date DATE,
        library_id INTEGER,
        FOREIGN KEY (library_id) REFERENCES Library(id)
    );

    CREATE TABLE Reader (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT,
        middle_name TEXT,
        address TEXT,
        phone TEXT,
        ticket_number TEXT UNIQUE,
        library_id INTEGER,
        FOREIGN KEY (library_id) REFERENCES Library(id)
    );

    CREATE TABLE Book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        genre TEXT,
        year INTEGER,
        total_copies INTEGER,
        library_id INTEGER,
        FOREIGN KEY (library_id) REFERENCES Library(id)
    );

    CREATE TABLE Loan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        reader_id INTEGER,
        librarian_id INTEGER,
        loan_date DATE,
        return_date DATE,
        status TEXT,
        FOREIGN KEY (book_id) REFERENCES Book(id),
        FOREIGN KEY (reader_id) REFERENCES Reader(id),
        FOREIGN KEY (librarian_id) REFERENCES Librarian(id)
    );
    """)

    conn.commit()
    print(" Tables created successfully!")


# ---------------------------- INSERT DATA ----------------------------

def insert_data(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    INSERT INTO Library (name, address, type, phone)
    VALUES ('Central Library', 'Kyiv, Main St. 10', 'public', '+380446664500');

    INSERT INTO Librarian (name, surname, position, hire_date, library_id)
    VALUES ('Olena', 'Kravets', 'Chief Librarian', '2020-05-10', 1);

    INSERT INTO Reader (name, surname, middle_name, address, phone, ticket_number, library_id)
    VALUES ('Taisiia', 'Rudyk', 'Andriivna', 'Kyiv, Heroiv St. 22', '+380501234567', 'T123', 1);

    INSERT INTO Book (title, author, genre, year, total_copies, library_id)
    VALUES ('1984', 'George Orwell', 'Dystopia', 1949, 5, 1);

    INSERT INTO Loan (book_id, reader_id, librarian_id, loan_date, return_date, status)
    VALUES (1, 1, 1, '2024-12-01', '2024-12-15', 'loaned');
    """)

    conn.commit()
    print(" Initial data inserted!")


# ---------------------------- SELECT QUERIES ----------------------------

def run_select_queries(conn):
    cursor = conn.cursor()

    print("\n SELECT: Список книг з їхніми читачами")
    rows = cursor.execute("""
        SELECT Book.title, Reader.name, Loan.loan_date
        FROM Loan
        JOIN Book ON Loan.book_id = Book.id
        JOIN Reader ON Loan.reader_id = Reader.id;
    """).fetchall()
    print(rows)

    print("\n SELECT: Всі читачі")
    print(cursor.execute("SELECT name, surname FROM Reader;").fetchall())

    print("\n SELECT: Список бібліотекарів")
    print(cursor.execute("SELECT name, surname FROM Librarian;").fetchall())


# ---------------------------- UPDATE ----------------------------

def update_query(conn):
    cursor = conn.cursor()
    print("\n✏ UPDATE: повернули книгу")

    cursor.execute("""
        UPDATE Loan
        SET status = 'returned'
        WHERE id = 1;
    """)
    conn.commit()

    print(" SELECT after UPDATE:")
    print(cursor.execute("SELECT * FROM Loan;").fetchall())


# ---------------------------- MAIN PROGRAM ----------------------------

if __name__ == "__main__":
    conn = create_connection("library.db")
    create_tables(conn)
    insert_data(conn)
    run_select_queries(conn)
    update_query(conn)
    conn.close()
    print("\n Program finished!")


