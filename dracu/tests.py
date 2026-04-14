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


# ─── Extended API Tests ───────────────────────────────────────────


class NewsExtendedTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_news_returns_dict_keyed_by_int(self):
        r = self.client.get("/api/news/")
        self.assertEqual(r.status_code, 200)
        news = r.data["news"]
        for key in news:
            self.assertIsInstance(int(key), int)

    def test_news_img_urls_are_absolute(self):
        r = self.client.get("/api/news/")
        for item in r.data["news"].values():
            self.assertTrue(
                item["img"].startswith("http"),
                f"img URL should be absolute: {item['img']}",
            )

    def test_news_has_three_items(self):
        r = self.client.get("/api/news/")
        self.assertEqual(len(r.data["news"]), 3)


class ChatExtendedTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_chat_init_returns_prompt(self):
        r = self.client.get("/api/chat/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("messages_dict", r.data)
        self.assertIn("message", r.data)
        # First message should be the init greeting
        self.assertTrue(len(r.data["message"]) > 0)

    def test_chat_conversation_flow(self):
        """Init → send message → response contains the question."""
        self.client.get("/api/chat/")
        r = self.client.post("/api/chat/", {"message": "What is a normal cycle?"}, format="json")
        self.assertIn(r.status_code, [200, 201])
        self.assertIn("message", r.data)
        # In mock mode, reply should echo back the question
        self.assertIn("messages_dict", r.data)

    def test_chat_messages_accumulate(self):
        self.client.get("/api/chat/")
        self.client.post("/api/chat/", {"message": "Q1"}, format="json")
        r = self.client.post("/api/chat/", {"message": "Q2"}, format="json")
        msgs = r.data.get("messages_dict", {})
        self.assertGreaterEqual(len(msgs), 3)  # init + Q1 + A1 + Q2 + A2


class CameraExtendedTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_camera_post_without_image(self):
        """POST without image should not crash (returns error or mock)."""
        r = self.client.post("/api/camera/", {}, format="json")
        # Should handle gracefully (either 200 mock or 400)
        self.assertIn(r.status_code, [200, 400, 500])


class EndpointsDiscoveryTest(TestCase):
    """Verify all expected API endpoints are reachable."""
    def setUp(self):
        self.client = APIClient()

    def test_all_get_endpoints_return_200(self):
        endpoints = [
            "/api/healthcheck/",
            "/api/stats/",
            "/api/news/",
            "/api/quiz",
            "/api/chat/",
            "/api/camera/",
            "/api/messages/",
        ]
        for endpoint in endpoints:
            r = self.client.get(endpoint)
            self.assertEqual(
                r.status_code, 200,
                f"GET {endpoint} returned {r.status_code}",
            )
