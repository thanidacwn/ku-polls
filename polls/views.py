from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from .models import Question, Choice, Vote
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def get_queryset(self):
    """show the last five question that not including those set
    to be published in the future"""
    return Question.objects.filter(
        pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class IndexView(generic.ListView):
    """ View for index page """
    template_name = 'polls/index.html'
    context_object_name = 'lastest_question_list'

    def get_queryset(self):
        """ Display the last five question in system"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """ View for detail page """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Not! include questions that are not published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """ Overide get method, check if question can be vote.

        Arguments:
            request {HTTP_REQUEST}

        Returns:
            httpResponse
        """
        error_msg = None
        user = request.user
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
        try:
            if not user.is_authenticated:
                raise Vote.DoesNotExist
            user_vote = question.vote_set.get(user=user).choice
        except Vote.DoesNotExist:
            # render to parent class (detail page)
            # render to error message 'You did not select a choice or invalid choice.'
            return super().get(request, *args, **kwargs)
        # go to detail page
        context = {
            'question': question,
            'user_vote': user_vote,
        }
        return render(request, 'polls/detail.html', context)


class ResultsView(generic.DetailView):
    """ View for results page """
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """ show the total votes for each choice. """
        return Question.objects.filter(pub_date__lte=timezone.now())


@login_required(login_url='/accounts/login')
def vote(request, question_id):
    """ voting for polls """
    user = request.user
    print("current user is", user.id, "login", user.username)
    # get question or throw error
    question = get_object_or_404(Question, pk=question_id)
    try:
        # if user didn't select vote choice,
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    # it will render you to detail page and show error messages.
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': 'You did not select a choice or invalid choice.',
        }
        return render(request, 'polls/detail.html', context)
    else:
        # check question can vote or not (expired or not)
        if question.can_vote():
            try:
                user_vote = question.vote_set.get(user=user)
                user_vote.choice = select_choice
                user_vote.save()
            except Vote.DoesNotExist:
                Vote.objects.create(
                                user=user,
                                choice=select_choice,
                                question=select_choice.question).save()
        else:
            # if question cannot vote(expired),
            # show error message and redirect to index page.
            messages.ERROR(request, 'You not allow to vote this question')
            return HttpResponseRedirect(reverse('polls:index'))
        # vote complete will redicrect to result page
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class EyesOnlyView(LoginRequiredMixin, generic.ListView):
    # this is the default. Same default as in auth_required decorator
    login_url = '/accounts/login/'
