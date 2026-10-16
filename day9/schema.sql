CREATE TABLE IF NOT EXISTS authors(
    author_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    copies INT NOT NULL,
    author_id INT,

    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

CREATE TABLE IF NOT EXISTS members(
    member_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS loans(
    loan_id INTEGER PRIMARY KEY,
    book_id INT,
    member_id INT,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    return_date DATE,
    status TEXT NOT NULL DEFAULT 'ISSUED'
        CHECK (status IN ('ISSUED', 'RETURNED')),

    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);