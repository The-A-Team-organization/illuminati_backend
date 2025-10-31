from django.urls import path
from .views import VotesTableView, SendVoteView, PromotionPermissionView, BanPermissionView, UserPromoteView, CloseActiveExpiredVotesView, UserBanView

urlpatterns = [
    path('getVotes/', VotesTableView.as_view(), name = 'votes-list'),
    path('sendVote/', SendVoteView.as_view(), name = 'send-vote'),
    path('hasPermission/', PromotionPermissionView.as_view(), name = 'has-permission'),
    path('banPermission/', BanPermissionView.as_view(), name = 'ban-permission'),
    path('promote/', UserPromoteView.as_view(), name = 'promote'),
    path('ban/', UserBanView.as_view(), name = 'ban-service'),
    path('vote_close/', CloseActiveExpiredVotesView.as_view(), name = 'vote_close'),
]
