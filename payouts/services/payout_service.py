from django.db import transaction
from typing import Optional

from payouts.models import Payout
from payouts.services.exceptions import PayoutStatusError
from payouts.repositories.payout_repository import PayoutRepository
from payouts.tasks import process_payout


class PayoutService:
    """Business logic for payouts."""

    def __init__(self, repository: Optional[PayoutRepository] = None) -> None:
        self._repository = repository or PayoutRepository()

    def list(self):
        return self._repository.list()

    def create(self, **payload: object) -> Payout:
        with transaction.atomic():
            payout = self._repository.create(**payload)
            transaction.on_commit(lambda: process_payout.delay(str(payout.id)))
            return payout

    def update_status(self, payout: Payout, status: str) -> Payout:
        if payout.status == Payout.Status.COMPLETED and status != payout.status:
            raise PayoutStatusError("Cannot change status after completion.")
        payout.status = status
        return self._repository.save(payout)
