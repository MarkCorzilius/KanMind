from django.urls import path, include
from boards_app.api.views import BoardListCreateView, BoardRetrieveUpdateDestroyView

urlpatterns = [
    path('', BoardListCreateView.as_view()),
    path('<int:pk>/', BoardRetrieveUpdateDestroyView.as_view()),
]