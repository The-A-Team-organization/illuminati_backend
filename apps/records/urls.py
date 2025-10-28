from django.urls import path
from .views import RecordListView, RecordCreateView, RecordDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("all", RecordListView.as_view(), name="records-all"),
    path("create", RecordCreateView.as_view(), name="records-create"),
    path("<int:record_id>", RecordDetailView.as_view(), name="records-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
