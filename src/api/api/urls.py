"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from booking.views import make_reservation, cancel_reservation, ScreeningViewSet
from ticketing.views import render_ticket
from paying.views import pay, refund
from api.views import dibs, dibs_two_phase_commit
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"screenings", ScreeningViewSet, basename="screening")

urlpatterns = [
    path("make-reservation", view=make_reservation),
    path("cancel-reservation", view=cancel_reservation),
    path("render-ticket", view=render_ticket),
    path("pay", view=pay),
    path("refund", view=refund),
    path("dibs", view=dibs),
    path("dibs-two-phase-commit", view=dibs_two_phase_commit),
] + router.urls
