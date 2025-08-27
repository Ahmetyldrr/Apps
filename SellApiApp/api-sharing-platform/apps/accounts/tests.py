from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class CustomUserTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_user_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')