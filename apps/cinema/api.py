from .services import recipe_generator
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import datetime
from apps.cinema import models
from .serializers import SzOnScreenOut, SzOnScreenIn
from . import cinema_mixins


class MovieViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    cinema_mixins.ReservationMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SzOnScreenOut

    def create(self, request, *args, **kwargs):
        serilizer = self.get_serializer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            db_reserve = self.reserve_seats(**serilizer.validated_data)
            if db_reserve:
                file_output_url = recipe_generator(request, serilizer.validated_data)
                print(file_output_url)
                return Response(
                    {"outUrl": file_output_url}, status=status.HTTP_201_CREATED
                )

        return Response({"message": "faild"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_serializer_class(self):
        match self.action:
            case "create":
                return SzOnScreenIn
            case _:
                return super().get_serializer_class()

    def get_queryset(self):
        date_query = self.request.query_params.get("date")
        if date_query:
            try:
                date_obj = datetime.strptime(date_query, "%B,%d,%Y").date()
                queryset = models.OnScreen.objects.filter(date=date_obj).select_related(
                    "movie"
                )

                return queryset

            except Exception as e:
                print(e)

        queryset = models.OnScreen.objects.filter(date=now().date()).select_related(
            "movie"
        )

        return queryset
