import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.models import Category
from src.models import Product


@pytest.fixture
def sample_products() -> list[Product]:
    return [
        Product("Товар 1", "Описание 1", 99.99, 5),
        Product("Товар 2", "Описание 2", 49.50, 10),
    ]


def test_product_initialization() -> None:
    product = Product("Ноутбук", "Игровой", 3999.99, 3)
    assert product.name == "Ноутбук"
    assert product.description == "Игровой"
    assert product.price == 3999.99
    assert product.quantity == 3


def test_category_initialization(sample_products: list[Product]) -> None:
    cat = Category("Электроника", "Устройства", sample_products)
    assert cat.name == "Электроника"
    assert cat.description == "Устройства"
    assert cat.products == sample_products


def test_category_product_count_reset(monkeypatch: MonkeyPatch, sample_products: list[Product]) -> None:
    # Сбросим значения общих атрибутов перед тестом
    monkeypatch.setattr(Category, "category_count", 0)
    monkeypatch.setattr(Category, "product_count", 0)

    Category("Категория 1", "Описание", sample_products)
    Category("Категория 2", "Описание", sample_products[:1])

    assert Category.category_count == 2
    assert Category.product_count == 3  # 2 товара + 1 товар
