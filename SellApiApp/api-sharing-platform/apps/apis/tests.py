from django.test import TestCase
from .models import Api

class ApiModelTest(TestCase):

    def setUp(self):
        self.api = Api.objects.create(
            name="Test API",
            description="This is a test API.",
            endpoint="https://api.test.com/v1/resource"
        )

    def test_api_creation(self):
        self.assertEqual(self.api.name, "Test API")
        self.assertEqual(self.api.description, "This is a test API.")
        self.assertEqual(self.api.endpoint, "https://api.test.com/v1/resource")

    def test_api_str(self):
        self.assertEqual(str(self.api), "Test API")