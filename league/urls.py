from .views import HomeView, LeagueView, TeamsView
from django.urls import path

urlpatterns = [
    # home
    path("", HomeView.as_view(), name="home"),
    path("league", LeagueView.as_view(), name="league"),
    path("teams", TeamsView.as_view(), name="teams"),
]
