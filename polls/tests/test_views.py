"""Test for views."""
from django.test import TestCase
from django.urls import reverse
from .test_base import create_question


class QuestionIndexViewTest(TestCase):
    """Test for question on index page."""

    def test_no_question(self):
        """If no question exist, show the messages."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_past_question(self):
        """Question with pub_date in the past are displayed on index view."""
        question = create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['lastest_question_list'],
                                 [question],)

    def test_two_past_question(self):
        """Index view must be show multiple questions."""
        question1 = create_question(question_text='Past question1', days=-30)
        question2 = create_question(question_text='Past question2', days=-25)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'],
                                 [question2, question1],)


class QuestionDetailViewTest(TestCase):
    """Test for question om detail page."""

    def test_future_question(self):
        """Question with a pub_date in the future in detail view will return 302 redirected."""
        future_question = create_question(question_text='Future question.',
                                          days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """Question with a pub_date in the past will show in detail view. It will return 302 redirected."""
        past_question = create_question(question_text='Past Question.',
                                        days=-10)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
