from django.urls import path
from .views import VotesTable, SendVote

urlpatterns = [
    path('getVotes/', VotesTable.as_view(), name='votes-list'),
    path('sendVote/', SendVote.as_view(), name='send-vote')
]
