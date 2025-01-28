from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer

User = get_user_model()


class JournalTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", password="password123")
        self.admin_user = User.objects.create(
            email="admin@mail.ru",
            password="adminpassword",
            is_staff=True,
            is_superuser=True,
        )
        self.diary_entry = DiaryEntry.objects.create(
            title="First Entry",
            content="This is my first diary entry.",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

        for i in range(10):  # Создаем 10 записей для тестирования пагинации
            DiaryEntry.objects.create(
                title=f"Entry {i + 1}",
                content=f"This is diary entry number {i + 1}",
                owner=self.user,
            )

    def test_create_diary_entry(self):
        response = self.client.post(
            "/journal/", {"title": "New Entry", "content": "This is a new diary entry."}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiaryEntry.objects.count(), 12)

    def test_view_own_diary_entries(self):
        response = self.client.get("/journal/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_view_single_own_diary_entry(self):
        response = self.client.get(f"/journal/{self.diary_entry.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.diary_entry.title)

    def test_update_own_diary_entry(self):
        response = self.client.patch(
            f"/journal/{self.diary_entry.id}/", {"title": "Updated Title"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diary_entry.refresh_from_db()
        self.assertEqual(self.diary_entry.title, "Updated Title")

    def test_delete_own_diary_entry(self):
        response = self.client.delete(f"/journal/{self.diary_entry.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DiaryEntry.objects.count(), 10)

    def test_admin_view_all_diary_entries(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/journal/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_admin_update_diary_entry(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            f"/journal/{self.diary_entry.id}/", {"title": "Admin Updated Title"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diary_entry.refresh_from_db()
        self.assertEqual(self.diary_entry.title, "Admin Updated Title")

    def test_admin_delete_diary_entry(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/journal/{self.diary_entry.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DiaryEntry.objects.count(), 10)

    def test_diary_entry_serializer(self):
        entry = DiaryEntry.objects.first()
        serializer = DiaryEntrySerializer(entry)
        self.assertEqual(serializer.data["title"], entry.title)
        self.assertEqual(serializer.data["content"], entry.content)
        self.assertEqual(serializer.data["owner"], entry.owner.id)
        self.assertIn(
            "created_at", serializer.data
        )  # Проверка на наличие поля created_at

    def test_pagination(self):
        response = self.client.get("/journal/?page=1&page_size=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 5
        )  # Проверяем количество записей на странице
        self.assertIn(
            "next", response.data
        )  # Проверяем наличие поля next для пагинации
        self.assertIn(
            "previous", response.data
        )  # Проверяем наличие поля previous для пагинации

    def test_pagination_with_multiple_pages(self):
        response = self.client.get("/journal/?page=2&page_size=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 5
        )  # Проверяем количество записей на странице

    def test_pagination_last_page(self):
        response = self.client.get("/journal/?page=3&page_size=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 1
        )  # Проверка последней страницы с нулевыми записями
