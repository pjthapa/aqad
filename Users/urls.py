from django.urls import path
from . import views

urlpatterns = [
    path('question/new/<int:user_id>', views.QuestionApi.get_question, name = 'Get New Question'),
    path('answer', views.QuestionApi.check_answer, name = 'Verify Correct Answer'),
    path('topic', views.change_topic, name ='Update a users question by topic id'),
    path('topic/create', views.populate_topics, name = 'Generate all new topics'),
    path('login/', views.login, name = 'Login'),
    path('get-csrf/', views.get_csrf, name='get_csrf'),
    path('topics/', views.get_all_topics, name='all-topics'),

]

