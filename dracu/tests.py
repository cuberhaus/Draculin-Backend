"""Tests for the Draculin Django REST API."""

from django.test import TestCase
from rest_framework.test import APIClient


class HealthCheckTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_healthcheck(self):
        r = self.client.get("/api/healthcheck/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["status"], "OK")


class StatsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_stats(self):
        r = self.client.get("/api/stats/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("stats", r.data)


class NewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_news(self):
        r = self.client.get("/api/news/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("news", r.data)
        news = r.data["news"]
        self.assertTrue(len(news) > 0)

    def test_news_has_fields(self):
        r = self.client.get("/api/news/")
        first = list(r.data["news"].values())[0]
        self.assertIn("title", first)
        self.assertIn("link", first)
        self.assertIn("img", first)


class QuizTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_quiz(self):
        r = self.client.get("/api/quiz")
        self.assertEqual(r.status_code, 200)
        self.assertIn("message", r.data)


class ChatTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_chat_init(self):
        r = self.client.get("/api/chat/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("message", r.data)

    def test_chat_post(self):
        self.client.get("/api/chat/")
        r = self.client.post("/api/chat/", {"message": "Hola"}, format="json")
        self.assertIn(r.status_code, [200, 201])
        self.assertIn("message", r.data)

    def test_chat_post_empty(self):
        self.client.get("/api/chat/")
        r = self.client.post("/api/chat/", {}, format="json")
        self.assertEqual(r.status_code, 400)


class CameraTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_camera_get(self):
        r = self.client.get("/api/camera/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("message", r.data)


class MessagesTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_messages_empty(self):
        r = self.client.get("/api/messages/")
        self.assertEqual(r.status_code, 200)

    def test_messages_after_chat(self):
        self.client.get("/api/chat/")
        r = self.client.get("/api/messages/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("messages_dict", r.data)
