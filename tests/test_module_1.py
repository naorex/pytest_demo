import sqlite3

from src.module_1 import add_numbers, all_books


def test_add_numbers_1():
    assert add_numbers(1, 2) == 3
    assert add_numbers(0, 0) == 0  # 複数書いてもOK
    # assert add_numbers(0, 0) == -1  # 成立しない場合はエラー（AssertionError）


def test_add_numbers_2():
    assert add_numbers(-1, -2) == -3


def test_all_books_1():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)")
    books = all_books(con)
    assert books == []
    con.close()
