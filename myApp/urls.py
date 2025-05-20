from . import views
from django.urls import path

app_name = "myApp"

urlpatterns = [
    path('', views.PollListView.as_view(), name='home'),
    path('poll/<int:pk>/', views.poll_view, name='poll'),
    path('create_poll/', views.create_poll, name='create_poll'),
]