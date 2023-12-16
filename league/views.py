import json
import csv
import os
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.shortcuts import render
from django.urls import reverse_lazy

from .backends import (
    TournamentController,
    TournamentDtoRequest,
    TeamsDtoRequest,
    TeamsController,
    StatisticController,
    RankController,
    UploadController,
)


# Create your views here.


class LoginView(BaseLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # if success redirect to home
        return reverse_lazy("home")


class LogoutView(BaseLogoutView):
    next_page = "login"

    def get_success_url(self):
        # if success redirect to home
        return reverse_lazy("login")


class HomeView(LoginRequiredMixin, TemplateView):
    # if user is not authenticated
    login_url = "login"
    redirect_field_name = "redirect_to"

    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class LeagueView(LoginRequiredMixin, View):
    # if user is not authenticated
    login_url = "login"
    redirect_field_name = "redirect_to"

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


class TeamsView(LoginRequiredMixin, View):
    # if user is not authenticated
    login_url = "login"
    redirect_field_name = "redirect_to"

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


class StatisticView(LoginRequiredMixin, View):
    # if user is not authenticated
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        cls = StatisticController()
        data = cls.get_statistic()
        return JsonResponse({"data": data}, status=HTTPStatus.OK)


class RankView(LoginRequiredMixin, View):
    # if user is not authenticated
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        cls = RankController()
        data = cls.calculate_rank()
        return JsonResponse({"data": data}, status=HTTPStatus.OK)


class UploadView(LoginRequiredMixin, View):
    # if user is not authenticated
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        """Download example csv"""
        file_path = os.path.join(
            os.path.dirname(__file__), UploadController.get_file_path()
        )
        with open(file_path, "rb") as file:
            response = HttpResponse(
                file.read(), content_type="application/octet-stream"
            )

        # Set the Content-Disposition header for download
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

    def post(self, request, *args, **kwargs):
        """Receive file upload and doing upsert to database"""
        file = request.FILES["file"]
        # Decode the file content and split it into lines
        decoded_file = file.read().decode("utf-8").splitlines()
        # Use the csv.reader to read the CSV content
        csv_reader = csv.reader(decoded_file)

        # process and build file from csv as list of dictionary
        records, headers = [], []
        for k, row in enumerate(csv_reader):
            # construct headers for first row
            if k == 0:
                headers = row
                continue

            records.append(dict(zip(headers, row)))

        # send the data for further process
        cls = UploadController.from_file(records)
        cls.store()
        return JsonResponse({"status": "ok"}, status=HTTPStatus.OK)
