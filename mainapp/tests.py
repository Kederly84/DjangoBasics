from http import HTTPStatus
from django.test.utils import override_settings
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail as django_mail

from authapp.models import User
from mainapp import tasks
from mainapp.models import News, Courses


class TestMainPage(TestCase):

    def test_page_open(self):
        path = reverse('mainapp:home')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class TestNewsPage(TestCase):
    fixtures = (
        "mainapp/fixtures/005_users.json",
        "mainapp/fixtures/001_news.json",
    )

    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse("authapp:login")
        self.client_with_auth.post(
            path_auth, data={"username": "django", "password": "GeekBrains"}
        )

    def test_page_open_list(self):
        path = reverse("mainapp:news")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_detail(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_detail", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_crete_deny_access(self):
        path = reverse("mainapp:news_create")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_crete_by_admin(self):
        path = reverse("mainapp:news_create")
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_create_in_web(self):
        counter_before = News.objects.count()
        path = reverse("mainapp:news_create")
        self.client_with_auth.post(
            path, data={
                "title": "NewTestNews001",
                "preambule": "NewTestNews001",
                "body": "NewTestNews001",
            },
        )
        self.assertGreater(News.objects.count(), counter_before)

    def test_page_open_update_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_in_web(self):
        new_title = "NewTestTitle001"
        news_obj = News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.post(
            path, data={
                "title": new_title,
                "preambule": news_obj.preambule,
                "body": news_obj.body,
            },
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


class TestTaskMailSend(TestCase):
    fixtures = ("mainapp/fixtures/005_users.json",)

    def test_mail_send(self):
        message_text = "test_message_text"
        user_obj = User.objects.first()
        tasks.send_feedback_mail(message_text, user_obj.pk)
        self.assertEqual(django_mail.outbox[0].body, message_text)


class CoursesDetailTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        for i in range(10):
            Courses.objects.create(
                name=f'name {i}',
                description=f'description {i}',
                cost=i
            )
        self.client = Client()

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache', }})
    def test_page_course_detail_open(self):
        course_obj = Courses.objects.first()
        path = reverse("mainapp:courses_detail", args=[course_obj.pk])
        print(path)
        print(course_obj)
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class LanguaugeChangeTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = Client()

    def test_change_language(self):
        self.response = self.client.post('/i18n/setlang/', {'language': 'en'}, follow=True)
        self.assertContains(self.response, 'Profile')
