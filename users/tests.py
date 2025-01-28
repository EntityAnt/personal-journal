from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserAPITestCase(APITestCase):

    def setUp(self):
        # Создание пользователя для тестирования
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "phone": "1234567890",
            "tg_nick": "testnick",
        }
        self.user = User.objects.create(**self.user_data)

    def test_user_registration(self):
        # url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "phone": "0987654321",
            "tg_nick": "newnick",
        }
        response = self.client.post("/users/", data)

        # Проверка статуса ответа
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка, что пользователь создан
        self.assertEqual(User.objects.count(), 1)

    # def test_user_login(self):
    #     # url = reverse('login')
    #     data = {
    #         "email": self.user.email,
    #         "password": self.user_data['password']
    #     }
    #     response = self.client.post("/users/", data)
    #     print(response)
    #
    #     # Проверка статуса ответа
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     # Проверка, что возвращается токен
    #     self.assertIn('access', response.data)
    #     self.assertIn('refresh', response.data)

    def test_user_detail(self):
        url = reverse("users:users-detail", args=[self.user.id])
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))
        response = self.client.get(url)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что возвращенные данные соответствуют пользователю
        self.assertEqual(response.data["email"], self.user.email)

    def test_user_update(self):
        url = reverse("users:users-detail", args=[self.user.id])
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))
        data = {"phone": "1111111111"}
        response = self.client.patch(url, data)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что пользователь был обновлен
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "1111111111")

    def test_user_delete(self):
        url = reverse("users:users-detail", args=[self.user.id])
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token))
        response = self.client.delete(url)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что пользователь был удален
        self.assertEqual(User.objects.count(), 0)
