import sqlite3


def read_integer(prompt, minimum=1):
    try:
        value = int(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None

    if value < minimum:
        print(f"Please enter a number greater than or equal to {minimum}.")
        return None

    return value


def add_book(conn):
    title = input("Enter the title of the book: ").strip()
    author = input("Enter the author of the book: ").strip()
    copies = read_integer("Enter the number of copies: ", minimum=0)
    if not title or not author or copies is None:
        print("Title, author, and a valid number of copies are required.")
        return

    try:
        conn.execute("BEGIN")
        author_row = conn.execute(
            "SELECT author_id FROM authors WHERE name = ?", (author,)
        ).fetchone()
        if author_row is None:
            cursor = conn.execute("INSERT INTO authors (name) VALUES (?)", (author,))
            author_id = cursor.lastrowid
        else:
            author_id = author_row[0]

        conn.execute(
            "INSERT INTO books (title, copies, author_id) VALUES (?, ?, ?)",
            (title, copies, author_id),
        )
        conn.commit()
        print("Book added successfully.")
    except sqlite3.Error as error:
        conn.rollback()
        print(f"Could not add the book: {error}")


def add_member(conn):
    name = input("Enter the member name: ").strip()
    email = input("Enter the member email: ").strip()
    if not name or not email:
        print("Member name and email are required.")
        return

    try:
        conn.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print("Member added successfully.")
    except sqlite3.IntegrityError as error:
        conn.rollback()
        if "members.email" in str(error):
            print(f"A member with email '{email}' already exists.")
        else:
            print(f"Could not add the member: {error}")
    except sqlite3.Error as error:
        conn.rollback()
        print(f"Could not add the member: {error}")


def view_books(conn):
    try:
        books = conn.execute(
            """
            SELECT books.book_id, books.title, authors.name, books.copies
            FROM books
            LEFT JOIN authors ON books.author_id = authors.author_id
            ORDER BY books.book_id
            """
        ).fetchall()
        if not books:
            print("No books found.")
            return

        print("Book ID | Title | Author | Available copies")
        for book_id, title, author, copies in books:
            print(f"{book_id} | {title} | {author or 'Unknown'} | {copies}")
    except sqlite3.Error as error:
        print(f"Could not view books: {error}")


def issue_book(conn):
    book_id = read_integer("Enter the book id: ")
    member_id = read_integer("Enter the member id: ")
    if book_id is None or member_id is None:
        return

    try:
        conn.execute("BEGIN IMMEDIATE")
        book = conn.execute(
            "SELECT copies FROM books WHERE book_id = ?", (book_id,)
        ).fetchone()
        if book is None:
            conn.rollback()
            print(f"Book {book_id} was not found.")
            return
        if book[0] <= 0:
            conn.rollback()
            print("This book has no copies available.")
            return

        member = conn.execute(
            "SELECT member_id FROM members WHERE member_id = ?", (member_id,)
        ).fetchone()
        if member is None:
            conn.rollback()
            print(f"Member {member_id} was not found.")
            return

        conn.execute(
            "INSERT INTO loans (book_id, member_id, status) VALUES (?, ?, 'ISSUED')",
            (book_id, member_id),
        )
        conn.execute(
            "UPDATE books SET copies = copies - 1 WHERE book_id = ?",
            (book_id,),
        )
        conn.commit()
        print("Book issued successfully.")
    except sqlite3.Error as error:
        conn.rollback()
        print(f"Could not issue the book: {error}")


def return_book(conn):
    loan_id = read_integer("Enter the loan id: ")
    if loan_id is None:
        return

    try:
        conn.execute("BEGIN IMMEDIATE")
        loan = conn.execute(
            "SELECT book_id, status FROM loans WHERE loan_id = ?", (loan_id,)
        ).fetchone()
        if loan is None:
            conn.rollback()
            print(f"Loan {loan_id} was not found.")
            return
        if loan[1] != "ISSUED":
            conn.rollback()
            print(f"Loan {loan_id} has already been returned.")
            return

        conn.execute(
            """
            UPDATE loans
            SET status = 'RETURNED', return_date = DATE('now')
            WHERE loan_id = ?
            """,
            (loan_id,),
        )
        conn.execute(
            "UPDATE books SET copies = copies + 1 WHERE book_id = ?", (loan[0],)
        )
        conn.commit()
        print("Book returned successfully.")
    except sqlite3.Error as error:
        conn.rollback()
        print(f"Could not return the book: {error}")


def main():
    try:
        conn = sqlite3.connect("library.db")
        conn.execute("PRAGMA foreign_keys = ON")
        loan_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(loans)").fetchall()
        }
        if "status" not in loan_columns:
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
            conn.commit()
    except sqlite3.Error as error:
        print(f"Could not connect to the library database: {error}")
        return

    try:
        while True:
            print(
                "\n1. Add a book\n"
                "2. Add a member\n"
                "3. View all books\n"
                "4. Issue a book\n"
                "5. Return a book\n"
                "6. Exit"
            )
            option = read_integer("Enter your choice: ")
            if option == 1:
                add_book(conn)
            elif option == 2:
                add_member(conn)
            elif option == 3:
                view_books(conn)
            elif option == 4:
                issue_book(conn)
            elif option == 5:
                return_book(conn)
            elif option == 6:
                break
            else:
                print("Please choose an option from 1 to 6.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
