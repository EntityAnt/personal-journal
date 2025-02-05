from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from journal.models import DiaryEntry

User = get_user_model()


class JournalViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовых пользователей
        cls.user = User.objects.create(
            email="testuser@test.com", password="testpass123"
        )
        cls.superuser = User.objects.create(
            password="adminpass123",
            email="admin@example.com",
            is_superuser=True,
            is_staff=True,
        )

        # Создаем тестовые записи
        cls.entry1 = DiaryEntry.objects.create(
            title="User Entry 1", content="Content 1", owner=cls.user
        )
        cls.entry2 = DiaryEntry.objects.create(
            title="Admin Entry", content="Content 2", owner=cls.superuser
        )

    def setUp(self):
        self.client = Client()

    # Тесты для JournalListView
    def test_journal_list_view_regular_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("journal:journal_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["object_list"], DiaryEntry.objects.filter(owner=self.user)
        )

    def test_journal_list_view_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("journal:journal_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["object_list"], DiaryEntry.objects.all(), ordered=False
        )

    # Тесты для JournalCreateView
    def test_create_view_regular_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("journal:entry_create"),
            {
                "title": "New Entry",
                "content": "New Content",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DiaryEntry.objects.count(), 2)
        # new_entry = DiaryEntry.objects.latest("created_at")
        # self.assertEqual(new_entry.owner, self.user)

    def test_create_view_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("journal:entry_create"),
            {"title": "Admin Entry", "content": "Admin Content", "owner": self.user.id},
        )
        self.assertEqual(response.status_code, 302)
        new_entry = DiaryEntry.objects.latest("created_at")
        self.assertEqual(new_entry.owner, self.user)

    def test_update_view_unauthorized_user(self):
        response = self.client.post(
            reverse("journal:entry_update", kwargs={"pk": self.entry2.pk}),
            {"title": "Hacked Entry", "content": "Hacked Content"},
        )
        self.assertEqual(response.status_code, 302)

    # Тесты для JournalDeleteView
    def test_delete_view_regular_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("journal:entry_delete", kwargs={"pk": self.entry1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DiaryEntry.objects.count(), 1)

    def test_delete_view_unauthorized_user(self):
        response = self.client.post(
            reverse("journal:entry_delete", kwargs={"pk": self.entry2.pk})
        )
        self.assertEqual(response.status_code, 302)

    # Тесты для JournalDetailView
    def test_detail_view_authorized_access(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("journal:entry_detail", kwargs={"pk": self.entry1.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_unauthorized_access(self):
        # self.client.logout()
        response = self.client.get(
            reverse("journal:entry_detail", kwargs={"pk": self.entry2.pk})
        )
        self.assertEqual(response.status_code, 302)

    # Тесты для поиска
    def test_search_functionality(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("journal:journal_list") + "?search=Content 1"
        )
        self.assertContains(response, "User Entry 1")
        self.assertNotContains(response, "Admin Entry")
