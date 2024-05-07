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

from django.shortcuts import redirect, render, get_object_or_404
from .models import Question, Tag, Answer

def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.page(page).object_list


# Create your views here.
def base(request):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)

    return render(request, 'base.html', {'popular_tags': popular_tags, 'popular_members': popular_members})
















from django.shortcuts import render, redirect
from .models import Tag, Question

from .forms import QuestionForm

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

            # Другие действия с данными, например, сохранение аватара

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
















from .forms import AnswerForm

def question(request, question_id):
    popular_tags = Tag.objects.get_popular_tags(count=5)
    popular_members = Profile.objects.get_popular_profiles(count=5)

    # Получаем объект вопроса
    question_obj = get_object_or_404(Question, pk=question_id)

    # Получаем теги для вопроса
    tags = question_obj.tags.all()

    # Получаем все ответы на этот вопрос
    answers = Answer.objects.filter(question=question_obj)

    if request.method == 'POST':
        # Если метод запроса POST, значит пользователь отправил форму с ответом
        form = AnswerForm(request.POST)
        if form.is_valid():
            # Получаем текст ответа из формы
            answer_content = form.cleaned_data['answer']

            # Создаем новый объект ответа в базе данных
            answer = Answer.objects.create(
                content=answer_content,
                author=request.user,
                question=question_obj
            )

            # После успешного добавления ответа, перенаправляем пользователя
            # на страницу с вопросом с прокруткой до нового ответа
            return redirect('question_with_scroll', question_id=question_id, answer_id=answer.id)
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

    return render(request, 'index.html', {'questions': paginate(quest, page), 'popular_tags': popular_tags, 'all_tags': all_tags, 'popular_members': popular_members})











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