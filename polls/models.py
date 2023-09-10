import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """ Question model """
    question_text = models.CharField(max_length=200)
    # default timezone.now in pub_date
    pub_date = models.DateTimeField('date published', default=timezone.now())
    end_date = models.DateTimeField('date ended', null=True, blank=True)
    available = models.BooleanField("poll available", default=True)

    @admin.display(
        boolean=True,
        ordering=['pub_date', 'end_date'],
        description='Published recently?',
    )
    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self):
        """Check that question was published less than 1 day or not.

        Returns:
            True if the question was published within the last day.
        """
        if not self.available:
            return False
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    def is_published(self):
        """Check that question is published or not by pub_date and currently.

        Returns:
            True if current date is on or after question's publication date.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check that voting is during pub_date and end_date, they can vote.

        Returns:
            True if voting is allowed for this question
        """
        # check end_date is not null
        if self.end_date:
            now = timezone.localtime()
            return self.end_date >= now and self.is_published
        return self.is_published()


class Choice(models.Model):
    """ Choice model """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """total vote for each choice"""
        return Vote.objects.filter(choice=self).count()

    def __str__(self) -> str:
        return self.choice_text


class Vote(models.Model):
    """ Voting models """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.user.username} --> {self.question.question_text}: {self.choice.choice_text}"
