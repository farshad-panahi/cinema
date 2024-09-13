from django.shortcuts import get_object_or_404
from .models import OnScreen

from django.db import transaction


class ReservationMixin:
    def reserve_seats(
        self, movie_id: int, slot: str, seat_numbers: list[int], *args, **kwds
    ) -> bool:
        try:
            movie = get_object_or_404(OnScreen, pk=movie_id)
            current_schedule = movie.seats
            if slot not in current_schedule:
                raise ValueError(
                    f"Slot '{slot}' does not exist for movie ID {movie_id}."
                )
            with transaction.atomic():
                for seat in set(seat_numbers):
                    seat_found = False
                    for seat_info in current_schedule[slot]:
                        if seat_info["seat_id"] == seat:
                            seat_found = True
                            if seat_info["status"] == "open":
                                seat_info["status"] = "closed"
                            else:
                                raise ValueError(f"Seat {seat} is already reserved.")
                            break

                    if not seat_found:
                        raise ValueError(
                            f"Seat {seat} does not exist in the selected slot."
                        )

                movie.seats = current_schedule
                movie.save()
                return True

        except Exception as e:
            print(f"Error reserving seats: {e}")
            return False
