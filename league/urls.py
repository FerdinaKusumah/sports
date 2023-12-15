from .views import HomeView, LeagueView, TeamsView, StatisticView, RankView
from django.urls import path

urlpatterns = [
    # home
    path("", HomeView.as_view(), name="home"),
    path("league", LeagueView.as_view(), name="league"),
    path("league/<uuid:id>", LeagueView.as_view(), name="league-update"),
    # teams url
    path("team", TeamsView.as_view(), name="team"),
    path("team/<uuid:id>", TeamsView.as_view(), name="team-update"),
    # statistic url
    path("statistic", StatisticView.as_view(), name="statistic"),
    # rank url
    path("rank", RankView.as_view(), name="rank"),
]
