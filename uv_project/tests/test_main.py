import requests


def test_main() -> None:
    assert True


def test_add_num(a: int = 2, b: int = 3) -> None:
    assert sum([a, b]) == 5
