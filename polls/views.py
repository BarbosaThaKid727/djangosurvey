from django import urls
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from lazysignup.decorators import allow_lazy_user

from .models import Choice, Question, UserResponse
from .utils import random_question


@allow_lazy_user
def index(request):
    context = {'question': random_question(request.user)}
    return render(request, 'polls/index.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/index.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        UserResponse.objects.create(
            user=request.user,
            choice=selected_choice,
            question=question,
        )
        redirect_url = urls.reverse('polls:index')
        return HttpResponseRedirect(redirect_url)
