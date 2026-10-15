import sqlite3

conn = None

try:
    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    inputs = [
        (1, 'John', 85),
        (2, 'Alice', 92),
        (3, 'Bob', 78),
        (4, 'Eve', 95),
        (5, 'Kavya', 51),
    ]
    c.executemany(
        'INSERT INTO students (id, name, marks) VALUES (?, ?, ?)',
        inputs,
    )

    c.execute('SELECT * FROM students')
    for row in c.fetchall():
        print(row)

    c.execute('SELECT * FROM students WHERE marks > 60')
    for row in c.fetchall():
        print(row)

    c.execute("UPDATE students SET marks = 100 WHERE name = 'Kavya'")
    c.execute("DELETE FROM students WHERE name = 'Bob'")

    c.execute('SELECT * FROM students')
    for row in c.fetchall():
        print(row)

    conn.commit()
    
except sqlite3.Error as error:
    print(f'Database error: {error}')
    if conn is not None:
        conn.rollback()
finally:
    if conn is not None:
        conn.close()