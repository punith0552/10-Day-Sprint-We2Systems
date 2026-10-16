
import sqlite3

conn=sqlite3.connect('library.db')

f=conn.cursor()

f.execute("PRAGMA foreign_keys = ON;")

f.execute("DROP TABLE IF EXISTS loans;")
f.execute("DROP TABLE IF EXISTS books;")
f.execute("DROP TABLE IF EXISTS members;")
f.execute("DROP TABLE IF EXISTS authors;")

with open('/Users/punith/Documents/10-Day-Sprint/day8/schema.sql','r') as file:
    sql_script = file.read()

f.executescript(sql_script)

print("Tables created successfully from schema.sql!")


f.execute("PRAGMA foreign_keys = ON;")

# 1. Insert 5 Authors (Parents to books)
authors_data = [
    ("J.K. Rowling",),
    ("George Orwell",),
    ("J.R.R. Tolkien",),
    ("Agatha Christie",),
    ("Dan Brown",)
]
f.executemany("INSERT OR IGNORE INTO authors (name) VALUES (?)", authors_data)

# 2. Insert 8 Books (References author_id 1 through 5)
books_data = [
    ("Harry Potter and the Sorcerer's Stone", 1, 5),
    ("Harry Potter and the Chamber of Secrets", 1, 3),
    ("1984", 2, 4),
    ("Animal Farm", 2, 2),
    ("The Hobbit", 3, 6),
    ("The Fellowship of the Ring", 3, 3),
    ("Murder on the Orient Express", 4, 4),
    ("The Da Vinci Code", 5, 5)
]

f.executemany("INSERT OR IGNORE INTO books (title, author_id, copies) VALUES (?, ?, ?)", books_data)

# 3. Insert 5 Members
members_data = [
    ("Alice Smith", "alice@email.com"),
    ("Bob Jones", "bob@email.com"),
    ("Charlie Brown", "charlie@email.com"),
    ("Diana Prince", "diana@email.com"),
    ("Ethan Hunt", "ethan@email.com")
]

f.executemany("INSERT OR IGNORE INTO members (name, email) VALUES (?, ?)", members_data)

# 4. Insert 5 Loans (Junction table linking book_id and member_id)
loans_data = [
    (1, 1),  # Book 1 loaned to Member 1
    (3, 2),  # Book 3 loaned to Member 2
    (5, 3),  # Book 5 loaned to Member 3
    (2, 4),  # Book 2 loaned to Member 4
    (7, 5)   # Book 7 loaned to Member 5
]
f.executemany("INSERT OR IGNORE INTO loans (book_id, member_id) VALUES (?, ?)", loans_data)

# Verify tables and printed output
tables = ["authors", "books", "members", "loans"]
for table in tables:
    print(f"\n--- Contents of {table} ---")
    f.execute(f"SELECT * FROM {table}")
    for row in f.fetchall():
        print(row)
        
conn.commit()