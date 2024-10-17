from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Choice, Question
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import QuestionForm, ChoiceForm

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def question_view(request):
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        choice_texts = request.POST.getlist('choice_text')

        if question_form.is_valid():
            question = question_form.save()

            for choice_text in choice_texts:
                if choice_text:
                    choice = Choice(question=question, choice_text=choice_text)
                    choice.save()

            return render(request, "polls/success.html")
    else:
        question_form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=str(i)) for i in range(3)]

    return render(request, 'polls/question_form.html', {
        'question_form': question_form,
        'choice_forms': choice_forms,
    })
