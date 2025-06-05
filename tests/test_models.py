import pytest
from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from src.models import Category
from src.models import LawnGrass
from src.models import Order
from src.models import Product
from src.models import Smartphone


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


# Тест на успешное сложение смартфонов
def test_smartphone_addition() -> None:
    s1 = Smartphone("iPhone", "Смартфон", 1000.0, 2, 95.0, "14 Pro", 256, "Серый")
    s2 = Smartphone("iPhone", "Смартфон", 1000.0, 1, 95.0, "14 Pro", 256, "Серый")
    result = s1 + s2
    assert result == 1000.0 * 3


# Тест на исключение при сложении разных типов товаров
def test_product_add_different_types() -> None:
    s = Smartphone("Samsung", "Смартфон", 800.0, 1, 80.0, "Galaxy S21", 128, "Черный")
    g = LawnGrass("GreenLife", "Трава", 100.0, 5, "Польша", "2 недели", "Зеленый")
    import pytest

    with pytest.raises(TypeError):
        _ = s + g


# Тест на успешное добавление LawnGrass в категорию
def test_add_lawngrass_to_category() -> None:
    grass = LawnGrass("EcoGrass", "Натуральная", 75.0, 4, "Германия", "10 дней", "Зеленый")
    category = Category("Сад", "Растения", [])
    category.add_product(grass)
    assert "EcoGrass, 75.0 руб. Остаток: 4 шт." in category.products


# Тест на запрет добавления не-продукта
def test_add_invalid_object_to_category() -> None:
    category = Category("Сад", "Растения", [])
    import pytest

    with pytest.raises(TypeError):
        category.add_product("непродукт")  # type: ignore[arg-type]


# проверяет корректное создание заказа, расчёт итоговой цены и уменьшение количества товара
def test_order_creation_and_total_price() -> None:
    product = Product("Мышка", "Беспроводная", 500.0, 10)
    order = Order("Заказ на мышку", "Покупка одной мышки", product, 1)
    assert order.name == "Заказ на мышку"
    assert order.description == "Покупка одной мышки"
    assert order.quantity == 1
    assert order.total_price == 500.0
    assert product.quantity == 9
    assert str(order) == "Заказ: Заказ на мышку — Мышка x 1 = 500.0 руб."


# проверяет, что попытка заказать больше, чем в наличии, вызывает ошибку
def test_order_exceeding_quantity_raises_error() -> None:
    product = Product("Монитор", "4K", 15000.0, 2)
    import pytest

    with pytest.raises(ValueError):
        Order("Слишком много", "Пытаемся купить 3", product, 3)


# Тест на проверку __repr__ через InitPrinterMixin
def test_product_repr_print(capsys: CaptureFixture[str]) -> None:
    Product("Планшет", "Android", 1200.0, 4)
    captured = capsys.readouterr()
    assert "Product создан с аргументами" in captured.out


# Тест на отрицательное количество в заказе
def test_order_negative_quantity_error() -> None:
    product = Product("Кресло", "Офисное", 1500.0, 1)
    import pytest

    with pytest.raises(ValueError):
        Order("Ошибка заказа", "Минус товар", product, 5)


# Тест на получение и установку корректной цены
def test_product_price_getter_setter() -> None:
    p = Product("Часы", "Наручные", 999.0, 1)
    p.price = 1200.0
    assert p.price == 1200.0


# Тест итерации по категории
def test_category_iterator(sample_products: list[Product]) -> None:
    cat = Category("Одежда", "Шапки", sample_products)
    names = [p.name for p in cat]
    assert names == ["Товар 1", "Товар 2"]


# Тест геттеров LawnGrass
def test_lawngrass_fields() -> None:
    grass = LawnGrass("BioGrass", "Экологичная", 85.0, 6, "Италия", "5 дней", "Зеленый")
    assert grass.country == "Италия"
    assert grass.germination_period == "5 дней"
    assert grass.color == "Зеленый"


# Тест геттеров Smartphone
def test_smartphone_fields() -> None:
    phone = Smartphone("Pixel", "Android", 1100.0, 3, 88.0, "Pixel 6", 128, "Черный")
    assert phone.efficiency == 88.0
    assert phone.model == "Pixel 6"
    assert phone.memory == 128
    assert phone.color == "Черный"


def test_product_with_zero_quantity_raises() -> None:
    import pytest
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Нулевой", "Без остатков", 999.0, 0)


def test_category_middle_price_empty() -> None:
    category = Category("Пустая", "Нет товаров", [])
    assert category.middle_price() == 0.0


def test_category_middle_price_valid() -> None:
    p1 = Product("Товар 1", "Тест", 100.0, 1)
    p2 = Product("Товар 2", "Тест", 200.0, 2)
    category = Category("Тестовая", "Есть товары", [p1, p2])
    assert category.middle_price() == 150.0

def test_category_class_counters(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Category, "product_count", 0)
    monkeypatch.setattr(Category, "category_count", 0)

    p1 = Product("A", "D", 100, 1)
    p2 = Product("B", "D", 200, 2)
    Category("Категория", "Описание", [p1, p2])

    assert Category.product_count == 2
    assert Category.category_count == 1


def test_category_class_counters(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Category, "product_count", 0)
    monkeypatch.setattr(Category, "category_count", 0)

    p1 = Product("A", "D", 100, 1)
    p2 = Product("B", "D", 200, 2)
    Category("Категория", "Описание", [p1, p2])

    assert Category.product_count == 2
    assert Category.category_count == 1


def test_category_iterator_object() -> None:
    p = Product("Товар", "Описание", 100.0, 1)
    category = Category("Категория", "Описание", [p])
    iterator = iter(category)
    assert next(iterator).name == "Товар"


def test_category_add_product_existing_name() -> None:
    p1 = Product("Книга", "1", 100.0, 1)
    p2 = Product("Книга", "2", 200.0, 2)
    category = Category("Книги", "Описание", [p1])
    category.add_product(p2)
    assert category.middle_price() == 150.0


def test_product_new_product_new_entry() -> None:
    existing = [Product("Телевизор", "OLED", 50000, 1)]
    data = {"name": "Наушники", "description": "BT", "price": 3000, "quantity": 1}
    new = Product.new_product(data, existing)
    assert new.name == "Наушники"
    assert new.quantity == 1
    existing.append(new)
    assert len(existing) == 2


def test_order_str() -> None:
    p = Product("Наушники", "Bluetooth", 3000.0, 5)
    order = Order("Заказ 1", "Покупка", p, 2)
    assert str(order) == "Заказ: Заказ 1 — Наушники x 2 = 6000.0 руб."


def test_category_iterator_stop_iteration() -> None:
    p = Product("Товар", "Описание", 100.0, 1)
    cat = Category("Категория", "Описание", [p])
    iterator = iter(cat)
    next(iterator)  # первый вызов — ок
    import pytest
    with pytest.raises(StopIteration):
        next(iterator)  # второй вызов — ошибка


def test_new_product_without_existing() -> None:
    data = {"name": "Мышь", "description": "Оптическая", "price": 500.0, "quantity": 1}
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "Мышь"
    assert product.quantity == 1


def test_price_setter_confirm_lower(monkeypatch: MonkeyPatch) -> None:
    p = Product("Товар", "Описание", 200.0, 1)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    p.price = 150.0
    assert p.price == 150.0


def test_price_setter_does_not_change_on_zero() -> None:
    p = Product("Тест", "Описание", 100.0, 1)
    p.price = 0.0
    assert p.price == 100.0