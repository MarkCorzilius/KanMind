from django.urls import path
from tasks_app.api.views import TaskCreateView, TasksAssignedToCurrentUserView, TasksReviewByCurrentUserView, TaskRetrieveUpdateDestroyView, CommentsListCreateViewSet


urlpatterns = [
    path('', TaskCreateView.as_view()),
    path('<int:task_pk>/', TaskRetrieveUpdateDestroyView.as_view()),
    path('assigned-to-me/', TasksAssignedToCurrentUserView.as_view()),
    path('reviewing/', TasksReviewByCurrentUserView.as_view()),
    path('<int:task_pk>/comments/', CommentsListCreateViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('<int:task_pk>/comments/<int:pk>/', CommentsListCreateViewSet.as_view({
        'delete': 'destroy'
    })),

]