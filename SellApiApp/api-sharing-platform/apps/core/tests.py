from django.test import TestCase
from .models import YourModel  # Replace with your actual model

class CoreModelTests(TestCase):

    def setUp(self):
        # Set up any initial data for your tests here
        self.model_instance = YourModel.objects.create(field1='value1', field2='value2')

    def test_model_str(self):
        # Test the string representation of the model
        self.assertEqual(str(self.model_instance), 'Expected String Representation')

    def test_model_field(self):
        # Test a specific field of the model
        self.assertEqual(self.model_instance.field1, 'value1')

    # Add more test methods as needed for your application logic