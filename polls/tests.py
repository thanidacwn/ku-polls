import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days=0, hours=0,  minutes=0, seconds=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTest(TestCase):
    """ Test for question model """

    def test_was_published_recently_with_future_question(self):
        """ return False for future question which pub_date in the future. """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ return False for old question which pub_date is older than 1 day. """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ return True for recent question which pub_date is within last day. """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """ return False, for question that publish date is in the future. """
        time = timezone.localtime() + datetime.timedelta(days=10)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_on_publish_time(self):
        """ return True, for question that current date/time is pub_date. """
        current_question = create_question('')
        self.assertIs(current_question.can_vote(), True)
        
    def test_cannot_vote_on_future_question(self):
        """ return True, for question that current date/time is in the future. """
        time = timezone.localtime()
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), True)

    def test_cannot_vote_on_expired_question(self):
        """ return False, for question that over end_date. """
        expired_question = create_question('', days=-1)
        time = timezone.localtime()
        expired_question.end_date = time - datetime.timedelta(days=1)
        self.assertIs(expired_question.can_vote(), False)


class QuestionIndexViewTest(TestCase):
    """ Test for question on index page """

    def test_no_question(self):
        """ If no question exist, show the messages. """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_past_question(self):
        """ Question with pub_date in the past are displayed on index view."""
        question = create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['lastest_question_list'], [question],)

    def test_future_question(self):
        """ Questions with pub_date in the future are not display on index view. """
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_future_question_and_past_question(self):
        """ If two questions exist, they will be display only past question."""
        past_question = create_question(question_text='Past question', days=-30)
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], [past_question],)

    def test_two_past_question(self):
        """ Index view must be show multiple questions. """
        question1 = create_question(question_text='Past question1', days=-30)
        question2 = create_question(question_text='Past question2', days=-25)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], [question2, question1],)


class QuestionDetailViewTest(TestCase):
    """ Test for question om detail page"""

    def test_future_question(self):
        """ Question with a pub_date in the future in detail view will return 302 redirected. """
        future_question = create_question(question_text='Future question.', days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """ Question with a pub_date in the past will show in detail view. """
        past_question = create_question(question_text='Past Question.', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
