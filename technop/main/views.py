from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Question

QUESTIONS = []
for i in range(0,100):
    QUESTIONS.append({
    'title': 'title ' + str(i),
    'id': i,
    'text': 'text' + str(i)
})
    
def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list

# Create your views here.
def base(request):
    return render(request, 'base.html')

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def question(request,question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item})

def index(request):
    quest = Question.objects.all()
    page = int(request.GET.get('page', 1))
    return render(request, 'index.html', {'questions': paginate(quest,page)})

def setting(request):
    return render(request, 'setting.html')