import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from .test_base import create_question


class QuestionModelTest(TestCase):
    """ Test for question model """

    def test_was_published_recently_with_future_question(self):
        """ return False for future question which pub_date in the future. """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ return False for old question
        which pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ return True for recent question
        which pub_date is within last day."""
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """ return False, for question that publish date is in the future."""
        time = timezone.localtime() + datetime.timedelta(days=10)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_past_question(self):
        """ return True, for question that publish date is in the past."""
        past_question = create_question('', days=-1)
        self.assertIs(past_question.is_published(), True)

    def test_is_published_with_default_pub_date(self):
        """ return True, for question that publish date is now"""
        now_question = create_question('')
        self.assertIs(now_question.is_published(), True)

    def test_can_vote_on_past_question(self):
        """ return True, for question that current date/time is in the past."""
        time = timezone.localtime() + timezone.timedelta(days=-1)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.can_vote(), True)

    def test_can_vote_on_publish_time(self):
        """ return True, for question that current date/time is pub_date. """
        current_question = create_question('')
        self.assertIs(current_question.can_vote(), True)

    def test_cannot_vote_on_future_question(self):
        """ return False, for question
        that current date/time is in the future."""
        time = timezone.localtime() + timezone.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), False)

    def test_cannot_vote_on_expired_question(self):
        """ return False, for question that over end_date."""
        expired_question = create_question('', days=-1)
        time = timezone.localtime()
        expired_question.end_date = time - datetime.timedelta(days=1)
        self.assertIs(expired_question.can_vote(), False)
