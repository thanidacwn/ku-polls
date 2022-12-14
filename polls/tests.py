import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Vote


def create_question(question_text, days, end=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_time = time+ datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_can_vote_now(self):
        """ test users is allowed to vote,
        if publish date is a current time """
        now = create_question(question_text="question1", days=0, end=7)
        self.assertIs(now.can_vote(), True)

    def test_can_vote_not_have_end_date(self):
        """ test users is allowed to vote, if poll not have end date """
        active_time = timezone.localtime() - datetime.timedelta(1)
        active_poll = Question(question_text="question1",
                               pub_date=active_time)
        self.assertIs(active_poll.can_vote(), True)

    def test_can_vote_is_publish_have_end_date(self):
        """ test users is allowed to vote, if poll is in voting period """
        poll = create_question(question_text="question1", days=-7, end=8)
        self.assertIs(poll.can_vote(), True)

    def test_can_not_vote_after_end_date(self):
        """ test users is not allowed to vote, after end date """
        poll_end = create_question(question_text="question1", days=-7)
        self.assertIs(poll_end.can_vote(), False)

    def test_can_not_vote_publish_date_in_future(self):
        """ test users is not allowed to vote, before publish date"""
        poll_future = create_question(question_text="question1", days=7)
        self.assertIs(poll_future.can_vote(), False)

    def test_can_not_vote_end_date_is_current(self):
        """ test users is not allowed to vote, if current is end date"""
        poll_passed = create_question(question_text="question", days=-7)
        self.assertIs(poll_passed.can_vote(), False)


class QuestionIndexViewTests(TestCase):

    def setUp(self) -> None:
        """Setup"""
        self.user = User.objects.create(username='computer1')
        self.user.set_password('password1')
        self.user.save()
        self.logged_in = self.client.login(
            username='computer1', password='password1')

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):

    def setUp(self) -> None:
        """Setup"""
        self.user = User.objects.create(username='computer1')
        self.user.set_password('password1')
        self.user.save()
        self.logged_in = self.client.login(
            username='computer1', password='password1')

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_user_can_vote_one(self):
        """ user can vote once per question """
        question = create_question("banana_question", days=-1)
        choice_1 = question.choice_set.create(choice_text="banana1")
        choice_2 = question.choice_set.create(choice_text="banana2")
        self.client.post(reverse('polls:vote', args=(question.id,)),
                         {'choice': choice_1.id})
        self.assertEqual(Vote.objects.get(user=self.user,
                         choice__in=question.choice_set.all(
                         )).choice, choice_1)
        self.assertEqual(Vote.objects.all().count(), 1)
        self.client.post(reverse('polls:vote', args=(question.id,)),
                         {'choice': choice_2.id})
        self.assertEqual(Vote.objects.get(user=self.user,
                         choice__in=question.choice_set.all(
                         )).choice, choice_2)
        self.assertEqual(Vote.objects.all().count(), 1)
