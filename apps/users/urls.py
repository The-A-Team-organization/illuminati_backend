from django.urls import path
from .views import UsersListView, UserDetailView, EmailView

urlpatterns = [
    path('', UsersListView.as_view(), name = 'users-list'),
    path('<int:user_id>/', UserDetailView.as_view(), name = 'user-detail'),
    path('participants/', EmailView.as_view(), name='participants-list'),
]
