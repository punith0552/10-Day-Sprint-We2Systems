# Library Management System

A Python and SQLite application for managing a small library's books, authors, members, and loans.
It tracks available copies as books are issued and returned, and provides SQL reports about the collection and borrowing activity.

## Database tables and relationships

- `authors`: one author can be associated with many books.
- `books`: each book references its author through `author_id`.
- `members`: stores library member names and unique email addresses.
- `loans`: each loan references one book and one member; a book or member can have many loans.

![Library database ER diagram](./er_diagram.png)

## Features

### App menu

1. Add a book (automatically adds a new author when needed).
2. Add a member (reports a clear message when the email is already registered).
3. View all books with author names and available copies.
4. Issue an available book to a member.
5. Return an issued book and restore its available copy.

### Reports

1. Currently issued books, with book title, member name, and issue date.
2. Number of books for each author.
3. Members who have borrowed more than one book.
4. Books that have never been issued.

The reports script also creates the `issued_books_view` view and an index on `loans.member_id` if they do not already exist.

## How to run

From this directory, run:

```bash
python setup_db.py
python app.py
python reports.py
```

The setup script creates and seeds `library.db` beside the scripts. It preserves existing records and can be run again safely.
