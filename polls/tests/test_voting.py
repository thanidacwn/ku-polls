"""Test for voting view."""
from django.test import TestCase
from django.urls import reverse
from polls.models import Vote
from django.contrib.auth.models import User
from .test_base import create_question


class VoteViewTest(TestCase):
    """Test for vote view."""

    def setUp(self) -> None:
        """Create user for test."""
        self.user = User.objects.create_user(username="demo_test")
        self.user.set_password("test123")
        self.user.save()
        self.client.login(username="demo_test", password="test123")

    def last_vote(self, user, question):
        """Return last vote of user."""
        return Vote.objects.filter(
            user=user, choice__in=question.choice_set.all()
        )

    def post_choice(self, user, choice):
        """Post choice for user."""
        url = reverse("polls:vote", args=(choice.question.id,))
        post_context = {"choice": choice.id}
        self.client.post(url, post_context)

    def test_vote_count(self):
        """Vote count must be increase by 1."""
        question = create_question("")
        choice = question.choice_set.create(choice_text='choice123')
        Vote.objects.create(question=question, choice=choice, user=self.user)
        self.assertEqual(choice.votes, 1)

    def test_can_vote_is_authenticated(self):
        """If user is already authenticated, user can vote, then status code: 202."""
        question = create_question("")
        url = reverse("polls:vote", args=(question.id,))
        selected_question = {"question": question.id}
        response = self.client.post(url, selected_question)
        self.assertEqual(response.status_code, 200)

    def test_user_get_only_one_vote_per_poll(self):
        """User can get only one vote for each question."""
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
        """If users already login, users can change their vote."""
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
