"""Importing the Question model and the timezone module from Django."""
import datetime
from django.utils import timezone
from polls.models import Question


def create_question(question_text, days=0, hours=0, minutes=0, seconds=0):
    """Create a question with the given `question_text` and publish it with the given number of `days` offset to now.

    Args:
        question_text (str): The text of the question.
        days (int): The number of days to offset the publication date.
        hours (int): The number of hours to offset the publication date.
        minutes (int): The number of minutes to offset the publication date.
        seconds (int): The number of seconds to offset the publication date.

    Returns:
        Question: The created Question object.
    """
    time = timezone.now() + datetime.timedelta(days=days,
                                               hours=hours,
                                               minutes=minutes,
                                               seconds=seconds)
    return Question.objects.create(question_text=question_text, pub_date=time)
