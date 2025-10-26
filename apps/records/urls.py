from django.urls import path
from .views import RecordListView

urlpatterns = [
    path("all", RecordListView.as_view(), name="records-all"),
]
