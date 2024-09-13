from django.shortcuts import render
from django.views import View
from django.conf import settings


class HomePage(View):
    def get(self, request):
        return render(request, "pages/home.html", context={"server": settings.SELF_URL})
