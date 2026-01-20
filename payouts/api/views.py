from rest_framework import status, viewsets
from rest_framework.response import Response

from payouts.api.serializers import (
    PayoutCreateSerializer,
    PayoutReadSerializer,
    PayoutUpdateSerializer,
)
from payouts.models import Payout
from payouts.services.payout_service import PayoutService


class PayoutViewSet(viewsets.ModelViewSet):
    serializer_class = PayoutReadSerializer
    lookup_field = "id"
    queryset = Payout.objects.all()

    def get_queryset(self):
        service = PayoutService()
        return service.list()

    def get_serializer_class(self):
        if self.action == "create":
            return PayoutCreateSerializer
        if self.action in {"partial_update", "update"}:
            return PayoutUpdateSerializer
        return PayoutReadSerializer

    def perform_create(self, serializer: PayoutCreateSerializer) -> None:
        service = PayoutService()
        payload = dict(serializer.validated_data)
        payload["status"] = Payout.Status.PENDING
        serializer.instance = service.create(**payload)

    def perform_update(self, serializer: PayoutUpdateSerializer) -> None:
        instance = serializer.instance
        service = PayoutService()

        if "status" in serializer.validated_data:
            service.update_status(instance, serializer.validated_data["status"])

        if "description" in serializer.validated_data:
            instance.description = serializer.validated_data["description"]
            instance.save(update_fields=["description", "updated_at"])

    def partial_update(self, request, *args, **kwargs):
        if not set(request.data.keys()).issubset({"status", "description"}):
            return Response(
                {"detail": "Only 'status' and 'description' can be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().partial_update(request, *args, **kwargs)
