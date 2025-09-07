import sqlite3


def add_numbers(a: int, b: int) -> int:
    return a + b


def all_books(con):
    books = con.execute("SELECT * FROM books").fetchall()
    con.close()
    return books


if __name__ == "__main__":
    print(add_numbers(1, 2))
