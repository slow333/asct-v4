from django.db.models import F
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Question, Choice
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from .forms import QuestionForm, ChoiceForm


def index(request):
    queryset = Question.objects.order_by("-pub_date")
    search_query = request.GET.get("searched", "")
    if search_query:
        queryset = queryset.filter(question_text__icontains=search_query)

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "polls/index.html", context)


def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, "polls/detail.html", {"question": question})


def create_poll(request):
    if request.method == "POST":
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            choice_texts = request.POST.getlist("choice_text")
            for text in choice_texts:
                if text.strip():
                    Choice.objects.create(question=question, choice_text=text)
            messages.success(request, "질문이 생성되었습니다.")
            blog_id = question.blog.id
            return redirect("blog:index")
    else:
        q_form = QuestionForm()
        c_form = ChoiceForm()
        return render(
            request, "polls/polls_form.html", {"q_form": q_form, "c_form": c_form}
        )


def update_poll(request, pk):
    question = get_object_or_404(Question, pk=pk)
    ChoiceFormSet = inlineformset_factory(
        Question, Choice, form=ChoiceForm, extra=0, can_delete=True
    )

    if request.method == "POST":
        q_form = QuestionForm(request.POST, instance=question)
        formset = ChoiceFormSet(request.POST, instance=question)
        if q_form.is_valid() and formset.is_valid():
            q_form.save()
            formset.save()
            choice_texts = request.POST.getlist("choice_text")
            for text in choice_texts:
                if text.strip():
                    Choice.objects.create(question=question, choice_text=text)
            messages.success(request, "질문이 수정되었습니다.")
            return redirect("blog:index")  # type: ignore
    else:
        q_form = QuestionForm(instance=question)
        formset = ChoiceFormSet(instance=question)
        c_form = ChoiceForm()
    return render(
        request,
        "polls/polls_form.html",
        {"q_form": q_form, "c_form": c_form, "formset": formset},
    )


def delete_poll(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    messages.success(request, "질문이 삭제되었습니다.")
    return redirect("blog:index")  # type: ignore


def result_poll(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, "polls/results.html", {"question": question})


def vote(request, pk):
    question = Question.objects.get(pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])  # type: ignore
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "선택해야 합니다.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        messages.success(
            request,
            f"투표가 완료되었습니다. {selected_choice.choice_text}를 투표했습니다.",
        )
        if question.blog:
            return redirect(reverse("blog:index") + f"?voted_pk={question.id}")  # type: ignore
        return redirect("polls:results", question.id)  # type: ignore
