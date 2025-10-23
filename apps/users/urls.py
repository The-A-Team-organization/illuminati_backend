from django.urls import path
from .views import UsersListView, UserDetailView

urlpatterns = [
    path('', UsersListView.as_view(), name = 'users-list'),
    path('<int:user_id>/', UserDetailView.as_view(), name = 'user-detail'),
]
