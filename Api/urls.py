from django.urls import path
from . import views

urlpatterns = [
    path("lesson/list", views.GetLessons.as_view()),
    path("lesson/info", views.GetAllInfoApi.as_view())
]