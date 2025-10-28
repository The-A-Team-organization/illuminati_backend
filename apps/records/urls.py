from django.urls import path
from .views import RecordListView, RecordCreateView, RecordDetailView

urlpatterns = [
    path("all", RecordListView.as_view(), name="records-all"),
    path("create", RecordCreateView.as_view(), name="records-create"),
    path("<int:record_id>", RecordDetailView.as_view(), name="records-detail"),
]
