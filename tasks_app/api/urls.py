from django.contrib import admin
from django.urls import path
from tasks_app.api.views import TaskCreateView, TasksAssignedToCurrentUserView, TasksReviewByCurrentUserView, TaskRetrieveUpdateDestroyView


urlpatterns = [
    path('', TaskCreateView.as_view()),
    path('<int:pk>/', TaskRetrieveUpdateDestroyView.as_view()),
    path('assigned-to-me/', TasksAssignedToCurrentUserView.as_view()),
    path('reviewing/', TasksReviewByCurrentUserView.as_view()),

]