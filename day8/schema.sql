Create table authors(
    author_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

Create table books(
    book_id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    copies INT NOT NULL,
    author_id INT,

    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

Create table members(
    member_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

Create table loans(
    loan_id INTEGER PRIMARY KEY,
    book_id INT,
    member_id INT,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    return_date DATE,

    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);