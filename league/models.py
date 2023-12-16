import uuid

from django.db import models


# Create your models here.
class Teams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True, unique=True)

    # manager models
    objects = models.Manager()  # The default manager.

    class Meta:
        db_table = "teams"
        verbose_name = "Team"
        verbose_name_plural = "Team"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    home = models.ForeignKey(
        Teams, on_delete=models.DO_NOTHING, related_name="home_tournament"
    )
    away = models.ForeignKey(
        Teams, on_delete=models.DO_NOTHING, related_name="away_tournament"
    )
    home_score = models.IntegerField(blank=True, null=True, default=0)
    away_score = models.IntegerField(blank=True, null=True, default=0)

    # manager models
    objects = models.Manager()  # The default manager.

    class Meta:
        db_table = "tournaments"
        verbose_name = "Tournaments"
        verbose_name_plural = "Tournaments"
        ordering = ["home"]

    def __str__(self):
        return f"{self.home.name}:{self.away.name}"
