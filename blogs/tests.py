from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import factory
from factory.django import DjangoModelFactory
from factory import Faker
from .models import Author, Post


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    password = Faker("password")


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    user = factory.SubFactory(UserFactory)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(AuthorFactory)
    title = Faker("sentence", nb_words=5)
    content = Faker("text")


class PostAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.author = AuthorFactory(user=self.user)
        self.post = PostFactory(author=self.author)
        self.client.force_authenticate(user=self.user)

    def test_list_posts(self):
        url = reverse('post_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post(self):
        url = reverse('post_detail', kwargs={'pk': self.post.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        url = reverse('post_list')
        data = {
            'title': 'Test post',
            'content': 'Test content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        url = reverse('post_detail', kwargs={'pk': self.post.id})
        data = {
            'title': 'Updated title',
            'content': 'Updated content'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        url = reverse('post_detail', kwargs={'pk': self.post.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)