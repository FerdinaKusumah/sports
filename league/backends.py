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
    def from_payload(
        cls, home_id: str, home_score: int, away_id: str, away_score: int
    ) -> "TournamentDtoRequest":
        """Initialize new object class
        :param home_id: string uuid for teams id as home
        :param home_score: int score for home team
        :param away_id: string uuid for teams as away
        :param away_score: int score for away team
        :return: instance class
        """
        return cls(home_id, home_score, away_id, away_score)

    @property
    def to_dict(self) -> dict[str, Any]:
        """Return class data as dictionary
        :return: dictionary data
        """
        return self.__dict__


class TeamsDtoRequest:
    name: str

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def from_payload(cls, name: str) -> "TeamsDtoRequest":
        """Initialize new object class
        :param name: string team name
        :return: instance class
        """
        return cls(name)

    @property
    def to_dict(self) -> dict[str, str]:
        """Return class data as dictionary
        :return: dictionary data
        """
        return self.__dict__


class TournamentController:
    def __init__(self, data: Union[TournamentDtoRequest, None]):
        self.data = data

    @classmethod
    def from_payload(cls, data: TournamentDtoRequest) -> "TournamentController":
        """Initialize new object Tournament model
        :param data: tournament data request
        :return: instance class
        """
        return cls(data)

    @classmethod
    def initialize(cls) -> "TournamentController":
        """Initialize new object Tournament model with empty param
        :return: instance class
        """
        return cls(None)

    @staticmethod
    def exists(id: str) -> bool:
        """Check if tournament data is exists for specified id
        :param id: string uuid for tournament id
        :return: boolean
        """
        return Tournament.objects.filter(id=id).exists()

    def list(self) -> list[dict[str, Any]]:
        """Get list of all tournament data
        :return: list of dictionary
        """
        # get all tournament order by teams name home and away
        queries = Tournament.objects.all().order_by("home__name", "away__name")

        resp = []
        for rec in queries:
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
        """Store new data and return the record id
        :return: string uuid for new record
        """
        record = Tournament.objects.create(**self.data.to_dict)
        return record.id

    def update(self, id: str) -> str:
        """Update specified tournament data and return record id
        :param id: string uuid data
        :return: string uuid for updated record
        """
        record = Tournament.objects.get(id=id)
        record.home_id = self.data.home_id
        record.away_id = self.data.away_id
        record.home_score = self.data.home_score
        record.away_score = self.data.away_score
        record.save()
        return record.id

    def delete(self, id: str) -> str:
        """Delete specified tournament data
        :param id: string uuid data
        :return: string uuid for deleted record
        """
        Tournament.objects.get(id=id).delete()
        return id


class TeamsController:
    def __init__(self, data: Union[TeamsDtoRequest, None]):
        self.data = data

    @classmethod
    def from_payload(cls, data: TeamsDtoRequest) -> "TeamsController":
        """Initialize new object Teams model
        :param data: teams data request
        :return: instance class
        """
        return cls(data)

    @classmethod
    def initialize(cls) -> "TeamsController":
        """Initialize new object Teams model with empty param
        :return: instance class
        """
        return cls(None)

    @staticmethod
    def exists(id: str) -> bool:
        """Check if eam data is exists for specified id
        :param id: string uuid record id
        :return: boolean
        """
        return Teams.objects.filter(id=id).exists()

    def list(self) -> list[dict[str, Any]]:
        """Get list of all tournament data
        :return: list of dictionary data
        """
        # get all teams and order by name
        queries = Teams.objects.all().order_by("name")

        resp = []
        for rec in queries:
            data = {"id": rec.id, "name": rec.name}
            resp.append(data)

        return resp

    def store(self) -> str:
        """Store new data and return the record id
        :return: string uuid of new record
        """
        record = Teams.objects.create(**self.data.to_dict)
        return record.id

    def update(self, id: str) -> str:
        """Update specified team data
        :param id: string uuid of record
        :return: string uuid of updated record
        """
        record = Teams.objects.get(id=id)
        record.name = self.data.name
        record.save()
        return record.id

    def delete(self, id: str) -> str:
        """Delete specified team data
        :param id: string uuid of record
        :return: string uuid of deleted record
        """
        Teams.objects.get(id=id).delete()
        return id


class StatisticController:
    def __init__(self):
        # we can move this max points to config to change the formula of points
        self.max_points = 3

    def get_statistic(self) -> list[dict[str, Any]]:
        """Calculate statistic for all teams
        to improve execution time we can separate by season, by datetime or divisions
            p -> means play
            w -> means win
            d -> means draw
            l -> means lose
            pts -> means total points
        :return: list of dictionary
        """
        # map all teams
        teams = {
            o.id.__str__(): {"name": o.name, "p": 0, "w": 0, "d": 0, "l": 0, "pts": 0}
            for o in Teams.objects.all()
        }

        # get tournament data
        queries = Tournament.objects.all()
        for tour in queries:
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

            # count points for home
            home_wins = teams[home_id]["w"] * self.max_points
            teams[home_id]["pts"] = home_wins + teams[home_id]["d"]

            # count points for away
            away_wins = teams[away_id]["w"] * self.max_points
            teams[away_id]["pts"] = away_wins + teams[away_id]["d"]

        return list(teams.values())


class RankController:
    # get top 5 from league rank
    # we can move this constant to config in we want dynamic show winner
    max_rank: int = 5

    @staticmethod
    def calculate_rank() -> list[dict[str, Any]]:
        """Sort teams based on higher points if have some points then sort by teams name
        this just using logic sorting after we get data from statistic about all teams information
        :return: list of top rank in league
        """
        cls = StatisticController()

        # sorted desc based on points and asc for team name
        resp = sorted(cls.get_statistic(), key=lambda x: (-x["pts"], x["name"]))

        ret = []
        # map value and return result
        for k, stat in enumerate(resp):
            # break if we have enough data for showing rank
            if RankController.max_rank == k:
                break

            ret.append({"rank": k + 1, "team": stat["name"], "point": stat["pts"]})

        return ret


class UploadController:
    # we can move this config to setting to make dynamic
    template_upload_path: str = "templates/upload/league.csv"

    def __init__(self, records: list[dict[str, Any]]):
        self.records = records

    @classmethod
    def from_file(cls, records: list[dict[str, Any]]) -> "UploadController":
        """Initialize new object class based on record that already extracted from csv file
        :param records: list of dictionary data extracted from csv
        :return: instance class
        """
        return cls(records)

    @staticmethod
    def get_file_path() -> str:
        """We provide download template for new users, as we can help them to provide correct template
        :return: string of local template that available in project
        """
        return UploadController.template_upload_path

    def populate_team_ids(self) -> dict[str, Any]:
        """This process is to provide teams_id for home and away
        we will search if data team in csv is available then we just provide the id
        if not we will insert and provide the id
        :return: dictionary data teams
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

        return teams

    def store(self) -> bool:
        """Store data to database using bulk create
        after mapping all available teams id we can
        directly insert all tournament data in one time
        :return: boolean
        """
        # populate data teams before inserting data
        teams = self.populate_team_ids()

        # now we can easily construct the data
        # and doing bulk insert
        records = []
        for rec in self.records:
            payload = Tournament(
                **{
                    "id": uuid.uuid4(),
                    "home_id": teams[rec["team_1_name"]]["id"],
                    "away_id": teams[rec["team_2_name"]]["id"],
                    "home_score": rec["team_1_score"],
                    "away_score": rec["team_2_score"],
                }
            )
            records.append(payload)

        # insert all data one time
        # here if the data is large we can use queue or chunking value
        Tournament.objects.bulk_create(records)
        return True
