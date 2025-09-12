import sqlite3
from pathlib import Path

import pytest
import requests

from src import module_1
from src.module_1 import add_numbers, all_books, get_user, get_user_names, write_note

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
# monkeypatch 機能を使う（自作関数に対して使う）
# ======================================


def test_get_user_names_1(monkeypatch):  # 引数に monkeypatch を指定しておく
    def mock_get_user(id):
        """モック"""
        print("start mock_get_user")
        return {"name": "鈴木"}

    # module_1 の get_user を mock_get_user に差し替える処理
    monkeypatch.setattr(module_1, "get_user", mock_get_user)
    assert get_user_names(["A001", "A002"]) == ["鈴木", "鈴木"]


# ======================================
# monkeypatch 機能を使う（外部関数に対して使う）
# ======================================


class MockResponse:
    def json(self):
        return {"name": "鈴木"}


def test_get_user_1(monkeypatch):
    def mock_get(url):
        """モック"""
        return MockResponse()

    # requests の get を mock_get に差し替える処理
    monkeypatch.setattr(requests, "get", mock_get)
    assert get_user("1") == {"name": "鈴木"}


# ======================================
# monkeypatch 機能を使う（その他機能）
# ======================================


def test_dir_1(tmp_path, monkeypatch):
    """
    カレントディレクトリを、テスト実行用の一時ディレクトリに変更するテストコード。テストが終わったら削除される。
    ここの引数の tmp_path は一時ディレクトリを提供する fixture であり、pathlib モジュールの Path オブジェクト。
    """
    monkeypatch.chdir(tmp_path)


def test_env_1(monkeypatch):
    """
    テスト実行用に一時的に環境変数を変更する。
    第1引数の値を、第2引数で指定した値に一時変更する。
    """
    monkeypatch.setenv("API_KEY", "test_api_key")


# ======================================
# 例外テスト
# ======================================


def test_write_note_1(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # 一時ディレクトリを使用

    # with の中でテスト対象の関数を呼び出して例外を発生させ、assert で意図通りかチェック
    with pytest.raises(FileNotFoundError) as e:
        write_note("test_data.txt", "あいうえお")
    assert str(e.value) == "test_data.txtが存在しません"
