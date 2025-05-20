from . import views
from django.urls import path

app_name = "myApp"

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
]