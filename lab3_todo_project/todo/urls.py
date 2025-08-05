from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskDetailView,
    TaskUpdateView, TaskDeleteView, UserProfileView
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('user/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
]
