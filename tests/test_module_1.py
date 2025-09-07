import sqlite3

import pytest

from src import module_1
from src.module_1 import add_numbers, all_books, get_user_names

# ======================================
# 単発テスト
# ======================================


def test_add_numbers_1():
    assert add_numbers(1, 2) == 3
    assert add_numbers(0, 0) == 0  # 複数書いてもOK
    # assert add_numbers(0, 0) == -1  # 成立しない場合はエラー（AssertionError）


def test_add_numbers_2():
    assert add_numbers(-1, -2) == -3


# ======================================
# fixture 機能を使う
# ======================================


def test_all_books_1():
    """使わない場合"""
    con = sqlite3.connect(":memory:")  # エラーがでるため一時的な接続でテスト
    con.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)")
    books = all_books(con)
    assert books == []
    con.close()


@pytest.fixture
def db_con():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)")
    return con


def test_all_books_1_w_fixture(db_con):
    """使う場合"""
    books = all_books(db_con)
    assert books == []
    db_con.close()


@pytest.fixture
def db_con_yield():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)")
    print("before yield")
    yield con  # -> return の代わりに yield と記述
    print("after yield")
    con.close()


def test_all_books_1_w_fixture_yield(db_con_yield):
    """使う場合"""
    books = all_books(db_con_yield)
    assert books == []


# ======================================
# monkeypatch 機能を使う
# ======================================


def test_get_user_names_1(monkeypatch):  # 引数に monkeypatch を指定しておく
    def mock_get_user(id):
        """モック"""
        print("start mock_get_user")
        return {"name": "鈴木"}

    # module_1 の get_user を mock_get_user に差し替える処理
    monkeypatch.setattr(module_1, "get_user", mock_get_user)
    assert get_user_names(["A001", "A002"]) == ["鈴木", "鈴木"]
