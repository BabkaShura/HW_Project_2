import unittest

from src.models import Smartphone, LawnGrass, Product


class TestProductInheritance(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(Smartphone, Product), "Smartphone не наследует Product")
        self.assertTrue(issubclass(LawnGrass, Product), "LawnGrass не наследует Product")

    def test_instance_creation(self):
        phone = Smartphone("iPhone", "Флагман Apple", 100000, 5, 0.9, "13 Pro", 128, "серый")
        self.assertIsInstance(phone, Smartphone)
        self.assertIsInstance(phone, Product)

        grass = LawnGrass("GreenGrass", "Для газона", 500, 20, "Нидерланды", "7 дней", "зеленый")
        self.assertIsInstance(grass, LawnGrass)
        self.assertIsInstance(grass, Product)

    def test_product_addition(self):
        p1 = Smartphone("iPhone", "Флагман", 100000, 2, 0.95, "14 Pro", 256, "черный")
        p2 = Smartphone("iPhone", "Флагман", 100000, 3, 0.95, "14 Pro", 256, "черный")
        total = p1 + p2
        self.assertEqual(total, 100000 * 5)

        with self.assertRaises(TypeError):
            p3 = LawnGrass("Grass", "Для сада", 100, 1, "Голландия", "10 дней", "зеленый")
            _ = p1 + p3

if __name__ == '__main__':
    unittest.main()
