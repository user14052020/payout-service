from django.db.models import QuerySet

from payouts.models import Payout


class PayoutRepository:
    """Data access layer for payouts."""

    def list(self) -> QuerySet[Payout]:
        return Payout.objects.all().order_by("-created_at")

    def get(self, payout_id: str) -> Payout:
        return Payout.objects.get(id=payout_id)

    def create(self, **kwargs: object) -> Payout:
        return Payout.objects.create(**kwargs)

    def save(self, payout: Payout) -> Payout:
        payout.save(update_fields=["status", "updated_at"])
        return payout
