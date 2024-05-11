from . import views
from django.urls import path

urlpatterns = [
    path('base', views.base),
    path('ask', views.ask),
    path('login', views.login_user, name='login'),
    path('signup', views.signup, name='register'),
    path('question/<int:question_id>', views.question, name='question'),
    path('index', views.index, name='index'),
    path('profile/edit', views.settings, name='settings'),
    path('tag/<int:tag_id>', views.tag_questions, name='tag_questions'),
    path('logout/', views.logout_view, name='logout'),
    path('question/<int:question_id>/scroll/<int:answer_id>', views.question_with_scroll, name='question_with_scroll'),
    # path('like_question/', views.like_question, name='like_question'),
    # path('set_correct_answer/', views.set_correct_answer, name='set_correct_answer'),





    path('question_like', views.like, name='like'),
    path('answer_like', views.answer_like, name='answer_like'),
    path('right_answer', views.right_answer, name='right_answer'),
]
