import json
from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .backends import (
    TournamentController,
    TournamentDtoRequest,
    TeamsDtoRequest,
    TeamsController,
    StatisticController,
    RankController,
)


# Create your views here.


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class LeagueView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        cls = TournamentController.from_payload(
            TournamentDtoRequest.from_payload(**data)
        )
        cls.store()
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def put(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return JsonResponse(
                {"message": "id is required"}, status=HTTPStatus.BAD_REQUEST
            )

        exists = TournamentController.exists(id=kwargs["id"])
        if not exists:
            return JsonResponse(
                {"message": "tournament is not found"}, status=HTTPStatus.BAD_REQUEST
            )

        data = json.loads(request.body)
        # check if score is minus
        if int(data["home_score"]) <= 0:
            return JsonResponse(
                {"message": "Home score cannot zero"}, status=HTTPStatus.BAD_REQUEST
            )

        if int(data["away_score"]) <= 0:
            return JsonResponse(
                {"message": "Away score cannot zero"}, status=HTTPStatus.BAD_REQUEST
            )

        cls = TournamentController.from_payload(
            TournamentDtoRequest.from_payload(**data)
        )
        cls.update(kwargs["id"])
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def delete(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return JsonResponse(
                {"message": "id is required"}, status=HTTPStatus.BAD_REQUEST
            )

        exists = TournamentController.exists(id=kwargs["id"])
        if not exists:
            return JsonResponse(
                {"message": "team is not found"}, status=HTTPStatus.BAD_REQUEST
            )

        cls = TournamentController.initialize()
        cls.delete(kwargs["id"])
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def get(self, request, *args, **kwargs):
        cls = TournamentController.initialize()
        data = cls.list()
        return JsonResponse({"data": data}, status=HTTPStatus.OK)


class TeamsView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        cls = TeamsController.from_payload(TeamsDtoRequest.from_payload(**data))
        cls.store()
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def put(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return JsonResponse(
                {"message": "id is required"}, status=HTTPStatus.BAD_REQUEST
            )
        exists = TeamsController.exists(id=kwargs["id"])
        if not exists:
            return JsonResponse(
                {"message": "team is not found"}, status=HTTPStatus.BAD_REQUEST
            )

        data = json.loads(request.body)
        cls = TeamsController.from_payload(TeamsDtoRequest.from_payload(**data))
        cls.update(kwargs["id"])
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def delete(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return JsonResponse(
                {"message": "id is required"}, status=HTTPStatus.BAD_REQUEST
            )
        exists = TeamsController.exists(id=kwargs["id"])
        if not exists:
            return JsonResponse(
                {"message": "team is not found"}, status=HTTPStatus.BAD_REQUEST
            )

        cls = TeamsController.initialize()
        cls.delete(kwargs["id"])
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)

    def get(self, request, *args, **kwargs):
        cls = TeamsController.initialize()
        data = cls.list()
        return JsonResponse({"data": data}, status=HTTPStatus.OK)


class StatisticView(View):
    def get(self, request, *args, **kwargs):
        cls = StatisticController()
        data = cls.get_statistic()
        return JsonResponse({"data": data}, status=HTTPStatus.OK)


class RankView(View):
    def get(self, request, *args, **kwargs):
        cls = RankController()
        data = cls.calculate_rank()
        return JsonResponse({"data": data}, status=HTTPStatus.OK)
