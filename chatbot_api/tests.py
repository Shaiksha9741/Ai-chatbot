from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ChatHistory

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_login(self):
        # Create a user
        User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            email=self.user_data['email']
        )
        
        # Login
        response = self.client.post(
            self.login_url, 
            {
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class ChatTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.chat_url = reverse('chat')
        self.chat_history_url = reverse('chat_history')
        
        # Login and get token
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpassword123'},
            format='json'
        )
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create some chat history
        ChatHistory.objects.create(
            user=self.user,
            user_message="Hello",
            bot_response="Hi there!"
        )
        ChatHistory.objects.create(
            user=self.user,
            user_message="How are you?",
            bot_response="I'm doing well, thank you!"
        )

    def test_get_chat_history(self):
        response = self.client.get(self.chat_history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
