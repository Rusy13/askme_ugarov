from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.urls import reverse
import requests
from django.conf import settings

from .models import Question, Answer, Tag, Profile, Like
from .forms import AnswerForm, QuestionForm, LoginForm, SignupForm, SettingsForm

def paginate(objects, request, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(1)
    return page_obj

def base(request):
    user = request.user
    return render(request, 'base.html', {'user': user})

@require_GET
def search_questions(request):
    query = request.GET.get('q', '')
    if query:
        results = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).values('id', 'title')[:10]
        suggestions = [{'id': result['id'], 'title': result['title']} for result in results]
        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'suggestions': []})

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
    return render(request, 'ask.html', {'form': form})

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
    return render(request, 'login.html', {'form': form})

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
            if password != password2:
                error_message = "Passwords do not match"
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
            if User.objects.filter(username=username).exists():
                error_message = "This username is already taken. Please choose another one."
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile.objects.create(user=user)
            if avatar:
                profile.avatar = avatar
                profile.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    next_url = request.GET.get('next', 'index')
    return redirect(next_url)

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
    question_obj = get_object_or_404(Question, pk=question_id)
    tags = question_obj.tags.all()
    answers = Answer.objects.filter(question=question_obj)
    new_answer_index = list(answers).index(Answer.objects.get(pk=answer_id))
    scroll_position = new_answer_index * 100
    redirect_url = reverse('question', kwargs={'question_id': question_id})
    redirect_url += f'#{scroll_position}'
    return redirect(redirect_url)

def index(request):
    quest = Question.objects.all()
    all_tags = [question.tags.all() for question in quest]
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        return redirect('index')
    latest_questions = Question.objects.get_latest()
    return render(request, 'index.html', {'questions': paginate(latest_questions, request, 5), 'all_tags': all_tags})

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
            profile = user.profile
            profile.avatar = avatar
            profile.save()
            return redirect('settings')
    else:
        form = SettingsForm(initial={'email': request.user.email, 'login': request.user.username})
    return render(request, 'settings.html', {'form': form})

def tag_questions(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    questions = tag.question_set.all()
    return render(request, 'tag_questions.html', {'tag': tag, 'questions': questions})

def answer_like(request):
    id = request.POST.get('answer_id')
    type = request.POST.get('value')
    is_positive = type == 'like'
    answer = get_object_or_404(Answer, pk=id)
    Like.objects.create(user=request.user, answer=answer, is_positive=is_positive)
    if is_positive:
        answer.rating += 1
    else:
        answer.rating -= 1
    answer.save()
    count = answer.rating
    return JsonResponse({'count': count})

def like(request):
    id = request.POST.get('question_id')
    type = request.POST.get('value')
    is_positive = type == 'like'
    question = get_object_or_404(Question, pk=id)
    Like.objects.create(user=request.user, question=question, is_positive=is_positive)
    if is_positive:
        question.rating += 1
    else:
        question.rating -= 1
    question.save()
    count = question.rating
    return JsonResponse({'count': count})

@login_required
def right_answer(request):
    question_id = request.POST.get('question_id')
    answer_id = request.POST.get('answer_id')
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == question.author:
        answer.is_correct = not answer.is_correct
        answer.save()
        return JsonResponse({'right_answer': answer.is_correct})
    else:
        return JsonResponse({'error': 'Only the question author can select the correct answer.'}, status=403)
