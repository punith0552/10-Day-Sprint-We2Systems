import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().with_name("library.db")


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


def print_report(conn, title, query):
    print(f"\n{title}")
    rows = conn.execute(query).fetchall()
    if not rows:
        print("No results.")
        return

    for row in rows:
        print(" | ".join(str(value) for value in row))


def main():
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            ensure_status_column(conn)
            conn.execute(
                """
                CREATE VIEW IF NOT EXISTS issued_books_view AS
                SELECT
                    books.title AS book_title,
                    members.name AS member_name,
                    loans.loan_date AS issue_date
                FROM loans
                JOIN books ON loans.book_id = books.book_id
                JOIN members ON loans.member_id = members.member_id
                WHERE loans.status = 'ISSUED'
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_loans_member_id
                ON loans(member_id)
                """
            )

            print_report(
                conn,
                "Report 1: Currently issued books (title | member | issue date)",
                """
                SELECT book_title, member_name, issue_date
                FROM issued_books_view
                ORDER BY issue_date, book_title
                """,
            )
            print_report(
                conn,
                "Report 2: Number of books per author (author | book count)",
                """
                SELECT authors.name, COUNT(books.book_id)
                FROM authors
                LEFT JOIN books ON authors.author_id = books.author_id
                GROUP BY authors.author_id, authors.name
                ORDER BY authors.name
                """,
            )
            print_report(
                conn,
                "Report 3: Members who borrowed more than one book (member | count)",
                """
                SELECT members.name, COUNT(loans.loan_id)
                FROM members
                JOIN loans ON members.member_id = loans.member_id
                GROUP BY members.member_id, members.name
                HAVING COUNT(loans.loan_id) > 1
                ORDER BY members.name
                """,
            )
            print_report(
                conn,
                "Report 4: Books that have never been issued (book | author)",
                """
                SELECT books.title, authors.name
                FROM books
                LEFT JOIN authors ON books.author_id = authors.author_id
                LEFT JOIN loans ON books.book_id = loans.book_id
                WHERE loans.loan_id IS NULL
                ORDER BY books.title
                """,
            )
    except sqlite3.Error as error:
        print(f"Could not generate library reports: {error}")


if __name__ == "__main__":
    main()
