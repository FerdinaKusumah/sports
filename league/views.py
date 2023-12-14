import json

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from http import HTTPStatus
from .models import Tournament, Teams

# Create your views here.


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class LeagueView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        Tournament.objects.create(**data)
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def get(self, request, *args, **kwargs):
        data = []
        for record in Tournament.objects.all():
            p = {
                "id": record.id,
                "home": record.home.name,
                "home_score": record.home_score,
                "away": record.away.name,
                "away_score": record.away_score,
            }
            data.append(p)
        return JsonResponse({"data": data}, status=HTTPStatus.OK)


class TeamsView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        Teams.objects.create(**data)
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def get(self, request, *args, **kwargs):
        data = []
        for record in Teams.objects.all():
            p = {"id": record.id, "home": record.name}
            data.append(p)
        return JsonResponse({"data": data}, status=HTTPStatus.OK)
