import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Vote
from django.contrib.auth.models import User


def create_question(question_text, days=0, hours=0,  minutes=0, seconds=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now.
    """
    time = timezone.now() + datetime.timedelta(days=days,
                                               hours=hours,
                                               minutes=minutes,
                                               seconds=seconds)
    return Question.objects.create(question_text=question_text, pub_date=time)


# def create_choice(question: Question, choice_text):
#     """Create a choice for a Question instance"""
#     return question.choice_set.create(choice_text=choice_text)


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
        self.assertQuerysetEqual(response.context['lastest_question_list'],
                                 [question],)

    def test_two_past_question(self):
        """ Index view must be show multiple questions. """
        question1 = create_question(question_text='Past question1', days=-30)
        question2 = create_question(question_text='Past question2', days=-25)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'],
                                 [question2, question1],)


class QuestionDetailViewTest(TestCase):
    """ Test for question om detail page"""

    def test_future_question(self):
        """ Question with a pub_date in the future in detail view
        will return 302 redirected. """
        future_question = create_question(question_text='Future question.',
                                          days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """ Question with a pub_date in the past will show in detail view.
        will return 302 redirected."""
        past_question = create_question(question_text='Past Question.',
                                        days=-10)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class VoteViewTest(TestCase):
    """Test for vote view"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="demo_test")
        self.user.set_password("test123")
        self.user.save()
        self.client.login(username="demo_test", password="test123")

    def last_vote(self, user, question):
        return Vote.objects.filter(
            user=user, choice__in=question.choice_set.all()
        )

    def post_choice(self, user, choice):
        url = reverse("polls:vote", args=(choice.question.id,))
        post_context = {"choice": choice.id}
        self.client.post(url, post_context)

    def test_vote_count(self):
        question = create_question("")
        choice = question.choice_set.create(choice_text='choice123')
        Vote.objects.create(question=question, choice=choice, user=self.user)
        self.assertEqual(choice.votes, 1)

    def test_can_vote_is_authenticated(self):
        """if user is already authenticated, user can vote,
        then status code: 202"""
        question = create_question("")
        url = reverse("polls:vote", args=(question.id,))
        selected_question = {"question": question.id}
        response = self.client.post(url, selected_question)
        self.assertEqual(response.status_code, 200)

    def test_user_get_only_one_vote_per_poll(self):
        """user can get only one vote for each question"""
        question = create_question(question_text="test")
        prev_choice = question.choice_set.create(choice_text="apple")
        recent_choice = question.choice_set.create(choice_text="banana")

        url1 = reverse("polls:vote", args=(question.id,))
        self.client.post(url1, {"choice": prev_choice.id})
        self.assertEqual(question.vote_set.get(user=self.user).choice, prev_choice)
        self.assertEqual(Vote.objects.all().count(), 1)

        url2 = reverse("polls:vote", args=(question.id,))
        self.client.post(url2, {"choice": recent_choice.id})
        self.assertEqual(question.vote_set.get(user=self.user).choice, recent_choice)
        self.assertEqual(Vote.objects.all().count(), 1)

    def test_user_can_change_their_vote(self):
        """if users already login, users can change their vote."""
        self.assertTrue(self.client)

        question = create_question("test")
        prev_choice = question.choice_set.create(choice_text="apple")
        recent_choice = question.choice_set.create(choice_text="banana")
        question.save()

        self.post_choice(self.user, prev_choice)
        self.assertEqual(self.last_vote(self.user, question).count(), 1)
        self.assertEqual(self.last_vote(self.user, question).get().choice, prev_choice)

        self.post_choice(self.user, recent_choice)
        # check vote is already count
        self.assertEqual(self.last_vote(self.user, question).count(), 1)
        # check vote is lasted vote
        self.assertEqual(self.last_vote(self.user, question).get().choice, recent_choice)
