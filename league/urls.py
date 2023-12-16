from .views import (
    HomeView,
    LeagueView,
    TeamsView,
    StatisticView,
    RankView,
    UploadView,
    LoginView,
    LogoutView,
)
from django.urls import path

urlpatterns = [
    # auth login
    path("login/", LoginView.as_view(), name="login"),
    # auth logout
    path("logout/", LogoutView.as_view(), name="logout"),
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
    # upload csv url
    path("upload", UploadView.as_view(), name="upload"),
]
