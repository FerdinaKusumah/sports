import uuid
from typing import Union, Any
from .models import Tournament, Teams


class TournamentDtoRequest:
    home_id: str
    home_score: int
    away_id: str
    away_score: int

    def __init__(self, home_id: str, home_score: int, away_id: str, away_score: int):
        self.home_id = home_id
        self.home_score = home_score
        self.away_id = away_id
        self.away_score = away_score

    @classmethod
    def from_payload(cls, **kwargs) -> "TournamentDtoRequest":
        """Initialize new object"""
        return cls(**kwargs)

    @property
    def to_dict(self):
        return self.__dict__


class TeamsDtoRequest:
    name: str

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def from_payload(cls, **kwargs) -> "TeamsDtoRequest":
        """Initialize new object"""
        return cls(**kwargs)

    @property
    def to_dict(self):
        return self.__dict__


class TournamentController:
    def __init__(self, data: Union[TournamentDtoRequest, None]):
        self.data = data

    @classmethod
    def from_payload(cls, data: TournamentDtoRequest) -> "TournamentController":
        """Initialize new object Tournament model"""
        return cls(data)

    @classmethod
    def initialize(cls) -> "TournamentController":
        """Initialize new object Tournament model"""
        return cls(None)

    @staticmethod
    def exists(id: str) -> bool:
        """Check if object is exists"""
        return Tournament.objects.filter(id=id).exists()

    def list(self) -> list[dict[str, Any]]:
        """Get list of all tournament data"""
        resp = []
        for rec in Tournament.objects.all().order_by("home__name", "away__name"):
            data = {
                "id": rec.id,
                "home": rec.home.name,
                "away": rec.away.name,
                "home_id": rec.home.id,
                "away_id": rec.away.id,
                "home_score": rec.home_score,
                "away_score": rec.away_score,
            }
            resp.append(data)

        return resp

    def store(self) -> str:
        """Store new data and return the id"""
        record = Tournament.objects.create(**self.data.to_dict)
        return record.id

    def update(self, id: str) -> str:
        """Update specified tournament data"""
        record = Tournament.objects.get(id=id)
        record.home_id = self.data.home_id
        record.away_id = self.data.away_id
        record.home_score = self.data.home_score
        record.away_score = self.data.away_score
        record.save()
        return record.id

    def delete(self, id: str) -> str:
        """Delete specified tournament data"""
        Tournament.objects.get(id=id).delete()
        return id


class TeamsController:
    def __init__(self, data: Union[TeamsDtoRequest, None]):
        self.data = data

    @classmethod
    def from_payload(cls, data: TeamsDtoRequest) -> "TeamsController":
        """Initialize new object Teams model"""
        return cls(data)

    @classmethod
    def initialize(cls) -> "TeamsController":
        """Initialize new object Teams model"""
        return cls(None)

    @staticmethod
    def exists(id: str) -> bool:
        """Check if object is exists"""
        return Teams.objects.filter(id=id).exists()

    def list(self) -> list[dict[str, Any]]:
        """Get list of all tournament data"""
        resp = []
        for rec in Teams.objects.all().order_by("name"):
            data = {"id": rec.id, "name": rec.name}
            resp.append(data)

        return resp

    def store(self) -> str:
        """Store new data and return the id"""
        record = Teams.objects.create(**self.data.to_dict)
        return record.id

    def update(self, id: str) -> str:
        """Update specified tournament data"""
        record = Teams.objects.get(id=id)
        record.name = self.data.name
        record.save()
        return record.id

    def delete(self, id: str) -> str:
        """Delete specified tournament data"""
        Teams.objects.get(id=id).delete()
        return id


class StatisticController:
    def __init__(self):
        self.max_points = 3

    def get_statistic(self) -> list[dict[str, Any]]:
        """Calculate statistic for all teams
        this one is example for simplicity
        to improve we can separate by season, by datetime or divisions
        :return: list of dictionary
        """
        # map all teams
        """
        p -> means play
        w -> means win
        d -> means draw
        l -> means lose
        pts -> means total points
        """
        teams = {
            o.id.__str__(): {"name": o.name, "p": 0, "w": 0, "d": 0, "l": 0, "pts": 0}
            for o in Teams.objects.all()
        }

        # get tournament data
        for tour in Tournament.objects.all():
            home_id = tour.home.id.__str__()
            away_id = tour.away.id.__str__()

            # count total play
            teams[home_id]["p"] += 1
            teams[away_id]["p"] += 1

            # count total wins
            teams[home_id]["w"] += tour.home_score > tour.away_score
            teams[away_id]["w"] += tour.away_score > tour.home_score

            # count total draw
            teams[home_id]["d"] += tour.home_score == tour.away_score
            teams[away_id]["d"] += tour.away_score == tour.home_score

            # count total lose
            teams[home_id]["l"] += tour.home_score < tour.away_score
            teams[away_id]["l"] += tour.away_score < tour.home_score

            # count points
            teams[home_id]["pts"] = (teams[home_id]["w"] * self.max_points) + teams[
                home_id
            ]["d"]
            teams[away_id]["pts"] = (teams[away_id]["w"] * self.max_points) + teams[
                away_id
            ]["d"]

        return list(teams.values())


class RankController:
    # get top 5 from league rank
    max_rank: int = 5

    @staticmethod
    def calculate_rank() -> list[dict[str, Any]]:
        """Sort teams based on higher points if have some points then sort by teams name"""
        cls = StatisticController()
        # sorted desc based on points and asc for team name
        resp = sorted(cls.get_statistic(), key=lambda x: (-x["pts"], x["name"]))
        # map value and return result
        ret = []
        for k, stat in enumerate(resp):
            if RankController.max_rank == k:
                break

            ret.append({"rank": k + 1, "team": stat["name"], "point": stat["pts"]})
        return ret


class UploadController:
    # we can change actual path in settings
    template_upload_path: str = "templates/upload/league.csv"

    def __init__(self, records: list[dict[str, Any]]):
        self.records = records
        self.cache = {}

    @classmethod
    def from_file(cls, records: list[dict[str, Any]]) -> "UploadController":
        return cls(records)

    @staticmethod
    def get_file_path() -> str:
        """return file path template upload"""
        return UploadController.template_upload_path

    def populate_team_ids(self):
        """Get teams id for each records
        here we can utilize using redis or some cache provider
        for this example we will user memory cache
        we will process the data in ON
        :return:
        """
        # assumption the data is valid
        teams = {}
        for rec in self.records:
            teams[rec["team_1_name"]] = rec["team_1_name"]
            teams[rec["team_2_name"]] = rec["team_2_name"]

        # check for all available teams
        db_teams = Teams.objects.filter(name__in=list(teams.values()))
        available_teams = {o.name: o.id.__str__() for o in db_teams}

        # now compare available vs file upload
        for team in teams.values():
            if team in available_teams:
                teams[team] = {"id": available_teams[team]}
            else:
                rec = Teams.objects.create(name=team)
                teams[team] = {"id": rec.id.__str__()}

        # store result to cache
        self.cache = teams

    def store(self) -> bool:
        """Store data to database"""
        # populate data teams before inserting data
        self.populate_team_ids()

        # now we can easily construct the data
        # and doing bulk insert
        records = []
        for rec in self.records:
            payload = Tournament(
                **{
                    "id": uuid.uuid4(),
                    "home_id": self.cache[rec["team_1_name"]]["id"],
                    "away_id": self.cache[rec["team_2_name"]]["id"],
                    "home_score": rec["team_1_score"],
                    "away_score": rec["team_2_score"],
                }
            )
            records.append(payload)

        # insert all data one time
        # here if the data is large we can use queue or chunking value
        Tournament.objects.bulk_create(records)
        return True
