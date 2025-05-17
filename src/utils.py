import json

from src.models import Category
from src.models import Product


def load_data_from_json(file_path: str) -> list[Category]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        products = [
            Product(name=prod["name"], description=prod["description"], price=prod["price"], quantity=prod["quantity"])
            for prod in category_data["products"]
        ]

        category = Category(name=category_data["name"], description=category_data["description"], products=products)
        categories.append(category)

    return categories


if __name__ == "__main__":
    categories = load_data_from_json("products.json")

    for cat in categories:
        print(f"\nКатегория: {cat.name}")
        print(f"Описание: {cat.description}")
        for product in cat.product_list:
            print(f"  - {product.name} ({product.price} руб., {product.quantity} шт.)")

    print(f"\nОбщее количество категорий: {Category.category_count}")
    print(f"Общее количество товаров: {Category.product_count}")
