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
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect, render, get_object_or_404
from .models import Question, Tag, Answer

from django.core.paginator import Paginator, EmptyPage, InvalidPage

def paginate(objects, request, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        # Если запрашиваемая страница не существует/некорректна, перенаправляем на первую страницу
        page_obj = paginator.page(1)
    return page_obj


# Create your views here.
from django.contrib.auth.models import User

def base(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    user = request.user  # Получаем объект текущего пользователя

    return render(request, 'base.html', {'popular_tags': popular_tags, 'popular_members': popular_members, 'user': user})








from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from .models import Question

@require_GET
def search_questions(request):
    query = request.GET.get('q', '')
    if query:
        # Поиск вопросов по заголовкам и содержимому
        results = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).values('id', 'title')[:10]  # Ограничиваем количество результатов до 10
        suggestions = [{'id': result['id'], 'title': result['title']} for result in results]
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})






from django.shortcuts import render, redirect
from .models import Tag, Question

from .forms import AnswerForm, QuestionForm

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            tags_input = form.cleaned_data['tags']

            tag_names = [tag.strip() for tag in tags_input.split(',')]

            question = Question.objects.create(
                title=title,
                content=text,
                author=request.user
            )

            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)

            question_id = question.id

            return redirect(reverse('question', kwargs={'question_id': question_id}))
    else:
        form = QuestionForm()

    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return render(request, 'ask.html', {'form': form, 'popular_tags': popular_tags, 'popular_members': popular_members})














from .forms import LoginForm

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return render(request, 'login.html', {'form': form, 'popular_tags': popular_tags, 'popular_members': popular_members})







from .forms import SignupForm

from django.contrib.auth.models import User
from .models import Profile  # Import the Profile model

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['login']
            email = form.cleaned_data['email']
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            avatar = form.cleaned_data['avatar']

            # Проверка на совпадение паролей
            if password != password2:
                error_message = "Passwords do not match"
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})

            # Проверка на существование пользователя с таким именем
            if User.objects.filter(username=username).exists():
                error_message = "This username is already taken. Please choose another one."
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})

            # Создание нового пользователя
            user = User.objects.create_user(username=username, email=email, password=password)

            # Создание профиля пользователя
            profile = Profile.objects.create(user=user)

            # Сохранение аватара, если он был загружен
            if avatar:
                profile.avatar = avatar
                profile.save()

            # Вход пользователя
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            # Перенаправление на главную страницу
            return redirect('index')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})








def logout_view(request):
    logout(request)
    # Получаем следующий URL из параметра запроса, если он есть, или перенаправляем на главную страницу
    next_url = request.GET.get('next', 'index')
    return redirect(next_url)




import requests

from django.conf import settings


def question(request, question_id):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    question_obj = get_object_or_404(Question, pk=question_id)
    tags = question_obj.tags.all()
    answers = Answer.objects.filter(question=question_obj)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_content = form.cleaned_data['answer']
            answer = Answer.objects.create(
                content=answer_content,
                author=request.user,
                question=question_obj
            )

            # Отправка сообщения в Centrifugo
            answer_data = {
                'answer': {
                    'author': {
                        'avatar_url': '/static/image/photo.jpg'
                    },
                    'content': answer.content
                }
            }
            centrifugo_api_url = 'http://localhost:8000/api'
            headers = {
                'Authorization': 'apikey 3d13d8d9-f550-4fab-b9c0-3276bb171c34'
            }
            requests.post(
                f'{centrifugo_api_url}/publish',
                json={
                    'channel': f'question_{question_id}',
                    'data': answer_data
                },
                headers=headers
            )

            return redirect('question', question_id=question_id)
    else:
        form = AnswerForm()

    return render(request, 'question.html', {
        'question': question_obj,
        'answers': answers,
        'form': form,
        'popular_tags': popular_tags,
        'tags': tags,
        'popular_members': popular_members
    })








def question_with_scroll(request, question_id, answer_id):
    # Получаем объект вопроса
    question_obj = get_object_or_404(Question, pk=question_id)

    # Получаем теги для вопроса
    tags = question_obj.tags.all()

    # Получаем все ответы на этот вопрос
    answers = Answer.objects.filter(question=question_obj)

    # Определяем индекс нового ответа
    new_answer_index = list(answers).index(Answer.objects.get(pk=answer_id))

    # Вычисляем, сколько пикселей нужно проскролить, чтобы новый ответ был виден
    scroll_position = new_answer_index * 100

    # Form the URL for the question with the scroll position
    redirect_url = reverse('question', kwargs={'question_id': question_id})
    redirect_url += f'#{scroll_position}'

    # Redirect the user to the question page with the scroll position
    return redirect(redirect_url)








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
    latest_questions = Question.objects.get_latest()
    return render(request, 'index.html', {'questions': paginate(latest_questions, request, 5), 'popular_tags': popular_tags, 'all_tags': all_tags, 'popular_members': popular_members})











from .forms import SettingsForm

def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            login = form.cleaned_data['login']
            nickname = form.cleaned_data['nickname']
            avatar = form.cleaned_data['avatar']

            user = request.user
            user.email = email
            user.username = login
            user.save()

            # Обновление URL аватарки в профиле пользователя
            profile = user.profile
            profile.avatar = avatar
            profile.save()

            return redirect('settings')
    else:
        form = SettingsForm(initial={'email': request.user.email, 'login': request.user.username})

    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)
    return render(request, 'settings.html', {'form': form, 'popular_tags': popular_tags, 'popular_members': popular_members})





def tag_questions(request, tag_id):
    # Получаем объект тега по его ID
    tag = get_object_or_404(Tag, pk=tag_id)
    # Получаем все вопросы, связанные с этим тегом
    questions = tag.question_set.all()
    return render(request, 'tag_questions.html', {'tag': tag, 'questions': questions})
















from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Question, Answer, Like

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Answer, Like

def answer_like(request):
    id = request.POST.get('answer_id')
    type = request.POST.get('value')
    if type == 'like':
        is_positive = True
    else:
        is_positive = False
    answer = get_object_or_404(Answer, pk=id)
    Like.objects.create(user=request.user, answer=answer, is_positive=is_positive)
    
    # Увеличить или уменьшить рейтинг ответа в зависимости от типа лайка
    if is_positive:
        answer.rating += 1
    else:
        answer.rating -= 1
    answer.save()  # Обновить рейтинг в базе данных
    
    count = answer.rating

    return JsonResponse({'count': count})


def like(request):
    id = request.POST.get('question_id')
    type = request.POST.get('value')
    if type == 'like':
        is_positive = True
    else:
        is_positive = False
    question = get_object_or_404(Question, pk=id)
    Like.objects.create(user=request.user, question=question, is_positive=is_positive)
    
    # Увеличить или уменьшить рейтинг в зависимости от типа лайка
    if is_positive:
        question.rating += 1
    else:
        question.rating -= 1
    question.save()  # Обновить рейтинг в базе данных
    
    count = question.rating

    return JsonResponse({'count': count})


from django.contrib.auth.decorators import login_required

@login_required
def right_answer(request):
    # Получаем ID вопроса и ID ответа из POST-запроса
    question_id = request.POST.get('question_id')
    answer_id = request.POST.get('answer_id')
    
    # Получаем объекты вопроса и ответа
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    
    # Проверяем, является ли текущий пользователь автором вопроса
    if request.user == question.author:
        # Если да, то продолжаем выполнение кода
        
        # Меняем правильный ответ на противоположное значение
        answer.is_correct = not answer.is_correct
        answer.save()
        
        # Возвращаем JsonResponse с новым значением is_correct
        return JsonResponse({'right_answer': answer.is_correct})
    else:
        # Если текущий пользователь не является автором вопроса,
        # возвращаем JsonResponse с сообщением об ошибке
        return JsonResponse({'error': 'Only the question author can select the correct answer.'}, status=403)
