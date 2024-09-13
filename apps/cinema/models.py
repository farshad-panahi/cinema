from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Movie(models.Model):
    def upload_path(self, instance):
        ins_ = instance.split(".")
        ins_[0] = self.name.replace("-", "")
        instance = ".".join(ins_)
        return "{}".format(instance)

    name = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", default=180)
    image = models.ImageField(
        storage=settings.LIARA_STORAGE(default_acl="public-read"), upload_to=upload_path
    )

    def __str__(self):
        return self.name


class OnScreen(models.Model):
    MORNING = "10:00-13:00"
    AFTERNOON = "14:00-17:00"
    EVENING = "20:00-23:00"

    TIME_SLOTS = ((MORNING, "morning"), (AFTERNOON, "afternoon"), (EVENING, "evening"))

    slots = ArrayField(
        models.CharField(choices=TIME_SLOTS, max_length=300, blank=False)
    )

    def get_default_schedule():
        number_of_seats = [{"seat_id": i, "status": "open"} for i in range(1, 51)]
        return {
            "10:00-13:00": number_of_seats.copy(),
            "14:00-17:00": number_of_seats.copy(),
            "20:00-23:00": number_of_seats.copy(),
        }

    seats = models.JSONField(default=get_default_schedule)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="scheduled")
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie", "date"], name="unique_movie")
        ]

    def __str__(self) -> str:
        return "{} at {}".format(self.movie.name, self.date)
