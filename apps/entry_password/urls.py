from django.urls import path
from .views import EntryView

urlpatterns = [
    path('entry_password/', EntryView.as_view(), name='entry_password'),
]