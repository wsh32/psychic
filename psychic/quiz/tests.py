import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.test.utils import setup_test_environment

from .models import Quiz


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_ok(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)


class TestQuizActive(TestCase):
    def test_quiz_active(self):
        time_now = timezone.now()
        time_pub = time_now - datetime.timedelta(days=1)
        time_exp = time_now + datetime.timedelta(days=1)

        quiz = Quiz(pub_date=time_pub, exp_date=time_exp)
        self.assertTrue(quiz.is_active())

    def test_quiz_not_published_yet(self):
        time_now = timezone.now()
        time_pub = time_now + datetime.timedelta(days=1)
        time_exp = time_now + datetime.timedelta(days=2)

        quiz = Quiz(pub_date=time_pub, exp_date=time_exp)
        self.assertFalse(quiz.is_active())

    def test_quiz_expired(self):
        time_now = timezone.now()
        time_pub = time_now - datetime.timedelta(days=2)
        time_exp = time_now - datetime.timedelta(days=1)

        quiz = Quiz(pub_date=time_pub, exp_date=time_exp)
        self.assertFalse(quiz.is_active())

