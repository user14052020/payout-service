from django.urls import include, path
from rest_framework.routers import DefaultRouter

from payouts.api.health import HealthCheckView
from payouts.api.views import PayoutViewSet


router = DefaultRouter()
router.register("payouts", PayoutViewSet, basename="payouts")

urlpatterns = [
    path("", include(router.urls)),
    path("health/", HealthCheckView.as_view(), name="healthcheck"),
]
