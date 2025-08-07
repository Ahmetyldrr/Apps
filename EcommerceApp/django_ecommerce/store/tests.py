from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            price=19.99,
            description="This is a test product.",
            image="path/to/image.jpg",
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.description, "This is a test product.")
        self.assertEqual(self.product.stock, 10)

    def test_product_stock_availability(self):
        self.assertTrue(self.product.is_in_stock)

        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock)