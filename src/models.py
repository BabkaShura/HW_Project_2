from typing import List
from typing import Optional


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if value < self.__price:
            confirm = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {value}? (y/n): ")
            if confirm.lower() != "y":
                print("Действие отменено")
                return
        self.__price = value

    @classmethod
    def new_product(cls, data: dict, existing_products: Optional[list["Product"]] = None) -> "Product":
        name = data["name"]
        description = data["description"]
        price = data["price"]
        quantity = data["quantity"]

        if existing_products is not None:
            for product in existing_products:
                if product.name == name:
                    # Обновляем количество и цену, если имя совпадает
                    product.quantity += quantity
                    product.price = max(product.price, price)
                    return product

        return cls(name, description, price, quantity)


class Category:
    # Атрибуты класса (общие для всех объектов)
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products

        # Увеличиваем общее количество категорий
        Category.category_count += 1

        # Увеличиваем общее количество товаров (по числу объектов Product в списке)
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт." for p in self.__products)

    @property
    def product_list(self) -> List[Product]:
        return self.__products
