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
    assert "Товар 1, 99.99 руб. Остаток: 5 шт." in cat.products
    assert "Товар 2, 49.5 руб. Остаток: 10 шт." in cat.products


def test_category_product_count_reset(monkeypatch: MonkeyPatch, sample_products: list[Product]) -> None:
    # Сбросим значения общих атрибутов перед тестом
    monkeypatch.setattr(Category, "category_count", 0)
    monkeypatch.setattr(Category, "product_count", 0)

    Category("Категория 1", "Описание", sample_products)
    Category("Категория 2", "Описание", sample_products[:1])

    assert Category.category_count == 2
    assert Category.product_count == 3  # 2 товара + 1 товар


# Тест для add_product
def test_add_product(sample_products: list[Product]) -> None:
    cat = Category("Электроника", "Гаджеты", sample_products[:1])
    new_product = Product("Товар 3", "Описание 3", 120.0, 7)
    cat.add_product(new_product)
    assert "Товар 3, 120.0 руб. Остаток: 7 шт." in cat.products


# Тест для Product.new_product: слияние количества и цены
def test_new_product_merge_quantity() -> None:
    existing = [Product("Книга", "Роман", 300.0, 5)]
    data = {"name": "Книга", "description": "Роман", "price": 250.0, "quantity": 2}
    product = Product.new_product(data, existing)
    assert product.quantity == 7
    assert product.price == 300.0  # Более высокая цена остается


# Тест для ограничения setter цены и подтверждения
def test_price_setter_invalid_and_confirm(monkeypatch: MonkeyPatch) -> None:
    p = Product("Принтер", "Цветной", 200.0, 4)

    # Попытка установить цену <= 0
    p.price = -10.0
    assert p.price == 200.0

    # Попытка понизить цену и отказ пользователя
    monkeypatch.setattr("builtins.input", lambda _: "n")
    p.price = 150.0
    assert p.price == 200.0

    # Подтверждение понижения цены
    monkeypatch.setattr("builtins.input", lambda _: "y")
    p.price = 150.0
    assert p.price == 150.0


# Тест для __str__ у Product
def test_product_str() -> None:
    product = Product("Телефон", "Смартфон", 999.99, 8)
    assert str(product) == "Телефон, 999.99 руб. Остаток: 8 шт."


# Тест для __str__ у Category
def test_category_str(sample_products: list[Product]) -> None:
    category = Category("Аксессуары", "Разное", sample_products)
    assert str(category) == "Аксессуары, количество продуктов: 15 шт."


# Тест для __add__ у Product
def test_product_add() -> None:
    p1 = Product("Монитор", "Full HD", 300.0, 2)
    p2 = Product("Клавиатура", "Механическая", 150.0, 3)
    result = p1 + p2
    assert result == 300.0 * 2 + 150.0 * 3  # 600 + 450 = 1050
