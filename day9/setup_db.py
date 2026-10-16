import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().with_name("library.db")
SCHEMA_PATH = Path(__file__).resolve().with_name("schema.sql")

AUTHORS = (
    "J.K. Rowling",
    "George Orwell",
    "J.R.R. Tolkien",
    "Agatha Christie",
    "Dan Brown",
)

BOOKS = (
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 5),
    ("Harry Potter and the Chamber of Secrets", "J.K. Rowling", 3),
    ("1984", "George Orwell", 4),
    ("Animal Farm", "George Orwell", 2),
    ("The Hobbit", "J.R.R. Tolkien", 6),
    ("The Fellowship of the Ring", "J.R.R. Tolkien", 3),
    ("Murder on the Orient Express", "Agatha Christie", 4),
    ("The Da Vinci Code", "Dan Brown", 5),
)

MEMBERS = (
    ("Alice Smith", "alice@email.com"),
    ("Bob Jones", "bob@email.com"),
    ("Charlie Brown", "charlie@email.com"),
    ("Diana Prince", "diana@email.com"),
    ("Ethan Hunt", "ethan@email.com"),
)

INITIAL_LOANS = (
    ("Harry Potter and the Sorcerer's Stone", "alice@email.com"),
    ("1984", "alice@email.com"),
    ("The Hobbit", "bob@email.com"),
    ("Animal Farm", "charlie@email.com"),
    ("The Da Vinci Code", "diana@email.com"),
)


def ensure_status_column(conn):
    columns = {
        row[1] for row in conn.execute("PRAGMA table_info(loans)").fetchall()
    }
    if "status" not in columns:
        conn.execute(
            """
            ALTER TABLE loans
            ADD COLUMN status TEXT NOT NULL DEFAULT 'ISSUED'
            CHECK (status IN ('ISSUED', 'RETURNED'))
            """
        )
        conn.execute(
            """
            UPDATE loans
            SET status = CASE
                WHEN return_date IS NULL THEN 'ISSUED'
                ELSE 'RETURNED'
            END
            """
        )


def main():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        ensure_status_column(conn)

        with conn:
            for name in AUTHORS:
                conn.execute(
                    """
                    INSERT INTO authors (name)
                    SELECT ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM authors WHERE name = ?
                    )
                    """,
                    (name, name),
                )

            author_ids = {
                name: conn.execute(
                    "SELECT author_id FROM authors WHERE name = ?", (name,)
                ).fetchone()[0]
                for name in AUTHORS
            }
            for title, author, copies in BOOKS:
                conn.execute(
                    """
                    INSERT INTO books (title, author_id, copies)
                    SELECT ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM books WHERE title = ? AND author_id = ?
                    )
                    """,
                    (title, author_ids[author], copies, title, author_ids[author]),
                )

            conn.executemany(
                "INSERT OR IGNORE INTO members (name, email) VALUES (?, ?)",
                MEMBERS,
            )

            has_loans = conn.execute(
                "SELECT 1 FROM loans LIMIT 1"
            ).fetchone()
            if has_loans is None:
                for title, email in INITIAL_LOANS:
                    book_id, copies = conn.execute(
                        "SELECT book_id, copies FROM books WHERE title = ?",
                        (title,),
                    ).fetchone()
                    member_id = conn.execute(
                        "SELECT member_id FROM members WHERE email = ?", (email,)
                    ).fetchone()[0]
                    if copies > 0:
                        conn.execute(
                            """
                            INSERT INTO loans (book_id, member_id, status)
                            VALUES (?, ?, 'ISSUED')
                            """,
                            (book_id, member_id),
                        )
                        conn.execute(
                            "UPDATE books SET copies = copies - 1 WHERE book_id = ?",
                            (book_id,),
                        )

        print(f"Database is ready: {DATABASE_PATH}")
    except (OSError, sqlite3.Error) as error:
        print(f"Could not set up the library database: {error}")
    finally:
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()
