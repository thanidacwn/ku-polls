import datetime
from django.utils import timezone
from polls.models import Question


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
