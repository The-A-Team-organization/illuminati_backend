from django.urls import path, include

urlpatterns = [
    path('authentific/', include('apps.authentific.urls')),
    path('users/', include('apps.users.urls')),
    path('entry_password/', include('apps.entry_password.urls')),
]
