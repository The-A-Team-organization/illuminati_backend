from django.urls import path
from .views import ChangeEntryView

urlpatterns = [
    path('set/', ChangeEntryView.as_view(), name='set'),
]