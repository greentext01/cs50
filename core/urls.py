from django.conf.urls import include
from django.urls.conf import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher/', views.teacher_dash, name='teacher'),
    path('create-period/', views.create_period, name='create_period'),
    path('create-homework/', views.create_homework, name='create_homework'),
    path('create-accounts/', views.create_accounts, name='create_accounts'),
    path('quiz/<int:id>/', views.quiz, name='quiz'),
    path('api/periods/<int:day>', views.get_periods, name='get_periods'),
    path('api/createquiz/', views.new_quiz, name='new_quiz'),
    path('api/assignments/', views.get_assignments, name='get_assignments'),
    path('api/finish/', views.set_finished, name='finish'),
    path('api/subjects/', views.get_subjects, name='students'),
    path('api/divisions/', views.get_divisions, name='divisions'),
    path('api/delete-period/<int:id>', views.delete_period, name='delete'),
]