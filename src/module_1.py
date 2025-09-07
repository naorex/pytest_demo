import requests


def add_numbers(a: int, b: int) -> int:
    return a + b


def all_books(con):
    books = con.execute("SELECT * FROM books").fetchall()
    con.close()
    return books


# ======================================
# モックテスト
# ======================================


def get_user(id: str) -> dict:
    response = requests.get(f"https://example.com/?id={id}")
    return response.json()


def get_user_names(ids: list[str]) -> list[str]:
    return [get_user(id)["name"] for id in ids]


if __name__ == "__main__":
    print(add_numbers(1, 2))
