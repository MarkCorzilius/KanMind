from django.contrib import admin
from django.urls import path
from tasks_app.api.views import TaskCreateView, TasksAssignedToCurrentUserView, TasksReviewByCurrentUserView


urlpatterns = [
    path('', TaskCreateView.as_view()),
    path('assigned-to-me/', TasksAssignedToCurrentUserView.as_view()),
    path('reviewing/', TasksReviewByCurrentUserView.as_view()),

]