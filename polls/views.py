from typing import Any
from django.db import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


def get_queryset(self):
    """show the last five question that not including those set to be published in the future"""
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lastest_question_list'

    def get_queryset(self):
        """ Display the last five question in system"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Not! include questions that are not published yet. """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """ show the total votes for each choice. """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    """ voting for polls """
    question = get_object_or_404(Question, pk=question_id) 
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': 'You did not select a choice.',
        }
        return render(request, 'polls/detail.html', context)
    else:
        # count vote for each select_choice
        select_choice.votes += 1
        select_choice.save()
        # Must!! return an HttpResponseRedirect after successfully dealing 
        # to prevent data posted twice if user click back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
