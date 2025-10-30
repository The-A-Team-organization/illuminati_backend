from django.urls import path
from .views import VotesTable, SendVote, PromotionPermission, BanPermission

urlpatterns = [
    path('getVotes/', VotesTable.as_view(), name = 'votes-list'),
    path('sendVote/', SendVote.as_view(), name = 'send-vote'),
    path('hasPermission/', PromotionPermission.as_view(), name = 'has-permission'),
    path('banPermission/', BanPermission.as_view(), name = 'ban-permission'),
]
