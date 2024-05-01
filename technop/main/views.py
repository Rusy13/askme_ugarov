from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Question
from .models import Answer
from .models import Tag
from .models import Profile
from django.http import Http404
from django.shortcuts import render, get_object_or_404


from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
    
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








def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        popular_tags = Tag.objects.get_popular_tags(count=5)
        popular_members = Profile.objects.get_popular_profiles(count=5)
        return render(request, 'login.html', {'popular_tags': popular_tags, 'popular_members': popular_members})








def signup(request):
    if request.method == 'POST':
        # Получение данных из POST-запроса
        username = request.POST.get('login')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        avatar = request.FILES.get('avatar')
        
        # Проверка на совпадение паролей
        if password != password2:
            error_message = "Passwords do not match"
            return render(request, 'signup.html', {'error_message': error_message})
        
        # Проверка на существование пользователя с таким именем
        if User.objects.filter(username=username).exists():
            error_message = "This username is already taken. Please choose another one."
            return render(request, 'signup.html', {'error_message': error_message})
        
        # Создание нового пользователя
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Другие действия с данными, например, сохранение аватара
        
        # Вход пользователя
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        
        # Перенаправление на главную страницу
        return redirect('index')
    else:
        return render(request, 'signup.html')








def logout_view(request):
    logout(request)
    # Получаем следующий URL из параметра запроса, если он есть, или перенаправляем на главную страницу
    next_url = request.GET.get('next', 'index')
    return redirect(next_url)




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











from django.core.exceptions import ObjectDoesNotExist

def settings(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        login = request.POST.get('login')
        nickname = request.POST.get('nickname')

        user = request.user

        user.email = email
        user.username = login
        user.save()

        return redirect('settings')

    else:
        popular_tags = Tag.objects.get_popular_tags(count=5)
        popular_members = Profile.objects.get_popular_profiles(count=5)
        return render(request, 'settings.html', {'popular_tags': popular_tags, 'popular_members': popular_members})








def tag_questions(request, tag_id):
    # Получаем объект тега по его ID
    tag = get_object_or_404(Tag, pk=tag_id)
    # Получаем все вопросы, связанные с этим тегом
    questions = tag.question_set.all()
    return render(request, 'tag_questions.html', {'tag': tag, 'questions': questions})