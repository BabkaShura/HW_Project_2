from typing import List
from typing import Optional


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного и того же типа.")
        return self.price * self.quantity + other.price * other.quantity

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
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его подклассов.")
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self) -> str:
        return "\n".join(str(p) for p in self.__products)

    @property
    def product_list(self) -> List[Product]:
        return self.__products

    def __iter__(self) -> "CategoryIterator":
        return CategoryIterator(self)


# доп задание
class CategoryIterator:
    def __init__(self, category: Category):
        self._products = category.product_list
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self._index < len(self._products):
            product = self._products[self._index]
            self._index += 1
            return product
        raise StopIteration


# Новые классы-наследники Product
class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
