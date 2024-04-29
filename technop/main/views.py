from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Question
from .models import Answer
from .models import Tag
from .models import Profile
from django.http import Http404
from django.shortcuts import render, get_object_or_404


    
def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list


# Create your views here.
def base(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)

    return render(request, 'base.html', {'popular_tags': popular_tags, 'popular_members': popular_members})

def ask(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return render(request, 'ask.html', {'popular_tags': popular_tags, 'popular_members': popular_members})

def login(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return render(request, 'login.html', {'popular_tags': popular_tags, 'popular_members': popular_members})

def signup(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return render(request, 'signup.html', {'popular_tags': popular_tags, 'popular_members': popular_members})

def question(request,question_id):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)

    try:
        
        quest = Question.objects.get(pk=question_id)
        ans = Answer.objects.get(pk=question_id)
        tags = quest.tags.all()
        # ans = Answer.objects.filter(question=quest)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    # quest = Question.objects.all()
    # item = quest[question_id-1]
    # ans = Answer.objects.all()
    # itemans = ans[question_id-1]
    return render(request, 'question.html', {'question': quest, 'answer': ans,'popular_tags': popular_tags,'tags': tags, 'popular_members': popular_members})


def index(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    quest = Question.objects.all()
    all_tags = [question.tags.all() for question in quest]
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        # Если параметр page не является числом, перенаправляем на главную страницу
        return redirect('index')

    return render(request, 'index.html', {'questions': paginate(quest, page), 'popular_tags': popular_tags, 'all_tags': all_tags, 'popular_members': popular_members})


def settings(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return render(request, 'settings.html', {'popular_tags': popular_tags, 'popular_members': popular_members})


def tag_questions(request, tag_id):
    # Получаем объект тега по его ID
    tag = get_object_or_404(Tag, pk=tag_id)
    # Получаем все вопросы, связанные с этим тегом
    questions = tag.question_set.all()
    return render(request, 'tag_questions.html', {'tag': tag, 'questions': questions})