from django.contrib import admin
from django import forms
from . import models


class OnScreenSlotsForm(forms.ModelForm):
    class Meta:
        model = models.Movie
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(OnScreenSlotsForm, self).__init__(*args, **kwargs)
        self.fields["slots"].widget = forms.CheckboxSelectMultiple(
            choices=models.OnScreen.TIME_SLOTS
        )

    def clean_slots(self):
        slots = self.cleaned_data.get("slots")
        if not slots:
            raise forms.ValidationError("Please select at least one slot.")
        return slots

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        slots = cleaned_data.get("slots")

        if date and slots:
            # Check for existing movies on selected date with the overlapping slots
            existing_movies = models.OnScreen.objects.filter(
                date=date, slots__overlap=slots
            )
            if existing_movies.exists():
                raise forms.ValidationError(
                    f"At least one slots conflicts- date {date}. check slots for today. every day on slot can be occupy by a movie."
                )

        return cleaned_data


@admin.register(models.OnScreen)
class OnScreenAdmin(admin.ModelAdmin):
    form = OnScreenSlotsForm
    list_display = ["js_format", "date", "movie", "slots"]

    def js_format(self, obj):
        import json

        return json.dumps(obj.seats, indent=2)[:100]

    def slots(self, obj):
        return ", ".join(obj.slots) if obj.slots else "No slots selected"

    slots.short_description = "Time Slots"


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "image")
