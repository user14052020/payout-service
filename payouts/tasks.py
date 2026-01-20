import time

from celery import shared_task
from django.db import transaction

from payouts.models import Payout


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def process_payout(self, payout_id: str) -> None:
    """Simulate payout processing and update status."""
    with transaction.atomic():
        try:
            payout = Payout.objects.select_for_update().get(id=payout_id)
        except Payout.DoesNotExist:
            return

        payout.status = Payout.Status.PROCESSING
        payout.save(update_fields=["status", "updated_at"])

    time.sleep(1)

    with transaction.atomic():
        try:
            payout = Payout.objects.select_for_update().get(id=payout_id)
        except Payout.DoesNotExist:
            return

        payout.status = Payout.Status.COMPLETED
        payout.save(update_fields=["status", "updated_at"])
