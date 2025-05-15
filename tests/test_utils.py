from pathlib import Path

from src.models import Category
from src.models import Product
from src.utils import load_data_from_json

TEST_JSON_PATH = Path(__file__).parent.parent / "src" / "products.json"


def test_load_data_from_json() -> None:
    Category.category_count = 0
    Category.product_count = 0
    # Загружаем данные из JSON
    categories = load_data_from_json(str(TEST_JSON_PATH))

    # Проверяем, что категории загружены правильно
    assert len(categories) > 0, "Должны быть загружены категории из JSON"

    # Проверка первой категории
    cat = categories[0]
    assert cat.name == "Смартфоны", "Название первой категории должно быть 'Смартфоны'"
    assert (
        cat.description
        == "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни"
    ), "Описание первой категории не совпадает"

    # Проверка товаров в категории
    assert len(cat.products) > 0, "Должны быть товары в категории"
    product = cat.products[0]
    assert isinstance(product, Product), "Продукты должны быть объектами класса Product"
    assert (
        product.name == "Samsung Galaxy C23 Ultra"
    ), "Название первого продукта должно быть 'Samsung Galaxy C23 Ultra'"
    assert product.price == 180000.0, "Цена первого продукта должна быть 180000.0"
    assert product.quantity == 5, "Количество первого продукта должно быть 5"

    # Проверяем количество категорий и товаров
    assert Category.category_count == len(categories), f"Должно быть {Category.category_count} категорий"
    total_products = sum(len(cat.products) for cat in categories)
    assert Category.product_count == total_products, f"Должно быть {Category.product_count} товаров"
