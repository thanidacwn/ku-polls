from django.db import models
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from .models import Question, Choice
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages


def get_queryset(self):
    """show the last five question that not including those set to be published in the future"""
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class IndexView(generic.ListView):
    """ View for index page """
    template_name = 'polls/index.html'
    context_object_name = 'lastest_question_list'

    def get_queryset(self):
        """ Display the last five question in system"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """ View for detail page """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Not! include questions that are not published yet. """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def get(self, request, *args, **kwargs):
        """ Overide get method, check if question can be vote.

        Arguments:
            request {HTTP_REQUEST}

        Returns:
            httpResponse
        """
        error_msg = None
        # get question or throw error
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            error_msg = '404'
        # check if question is expired, then show error message and redirect to index page.
        if not question.can_vote() or error_msg == '404':
            messages.error(request, 'This question not allow to vote for now.')
            return HttpResponseRedirect(reverse('polls:index'))
        # else
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """ View for results page """
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """ show the total votes for each choice. """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    """ voting for polls """
    # get question or throw error
    question = get_object_or_404(Question, pk=question_id) 
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    # if user didn't select vote choice, 
    # it will render you to detail page and show error messages.
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': 'You did not select a choice.',
        }
        return render(request, 'polls/detail.html', context)
    else:
        # check question can vote or not (expired or not)
        if question.can_vote():
            # count vote for each select_choice
            select_choice.votes += 1
            select_choice.save()
            # Must!! return an HttpResponseRedirect after successfully dealing 
            # to prevent data posted twice if user click back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else:
            # if question cannot vote(expired), show error message and redirect to index page.
            messages.ERROR(request, 'You not allow to vote this question')
            return HttpResponseRedirect(reverse('polls:index'))
