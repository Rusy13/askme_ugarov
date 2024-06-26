from . import views
from django.urls import path

urlpatterns = [
    path('base', views.base),
    path('ask', views.ask),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='register'),
    path('question/<int:question_id>', views.question, name='question'),
    path('index', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('tag/<int:tag_id>', views.tag_questions, name='tag_questions'),
]
