from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK)


CREATE_USER_URL = reverse('user:create')
TOKEN_USER_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with the valid payload is successful"""

        payload = {
            'email': 'test@test.com',
            'password': 'password',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""

        payload = {
            'email': 'test@test.com',
            'password': 'password'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""

        payload = {
            'email': 'test@test.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""

        payload = {
            'email': 'test@test.com',
            'password': 'password'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_USER_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""

        create_user(email='test@test.com', password='password')

        payload = {
            'email': 'test@test.com',
            'password': 'wrong'
        }

        res = self.client.post(TOKEN_USER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""

        payload = {
            'email': 'test@test.com',
            'password': 'password'
        }

        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test that email and password are required"""

        res = self.client.post(TOKEN_USER_URL, {
            'email': 'test',
            'password': ''
        })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
