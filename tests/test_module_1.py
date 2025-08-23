from src.module_1 import add_numbers


def test_add_numbers_1():
    assert add_numbers(1, 2) == 3
    assert add_numbers(0, 0) == 0  # 複数書いてもOK
    # assert add_numbers(0, 0) == -1  # 成立しない場合はエラー（AssertionError）


def test_add_numbers_2():
    assert add_numbers(-1, -2) == -3
