from rest_framework import serializers
from apps.cinema import models


class SzMovieOut(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = "__all__"


class SzOnScreenOut(serializers.ModelSerializer):
    movie = SzMovieOut()

    class Meta:
        model = models.OnScreen
        fields = ["id", "date", "movie", "seats", "slots"]


class SzMovieIn(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = [
            "id",
        ]


class SzOnScreenIn(serializers.ModelSerializer):
    movie_id = serializers.IntegerField()
    seat_numbers = serializers.ListField(child=serializers.IntegerField())
    slot = serializers.CharField()
    date = serializers.CharField()
    frmt = serializers.CharField()
    movie_name = serializers.CharField()

    def validate_seat_numbers(self, value):
        if any(num < 1 or num > 50 for num in value):
            raise serializers.ValidationError("seat numbers must be between 1 and 50.")
        return value

    def validate_frmt(self, value):
        available_formats = ("pdf", "epub")
        if value not in available_formats:
            raise serializers.ValidationError("this format is not supported")
        return value

    class Meta:
        model = models.OnScreen
        fields = ["movie_id", "slot", "seat_numbers", "date", "frmt", "movie_name"]
