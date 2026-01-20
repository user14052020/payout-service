from django.core.management.base import BaseCommand

from payouts.models import Payout


class Command(BaseCommand):
    help = "Seed initial payout data."

    def handle(self, *args, **options):
        if Payout.objects.exists():
            self.stdout.write(self.style.WARNING("Payouts already exist, skipping."))
            return

        payouts = [
            Payout(
                amount="100.00",
                currency=Payout.Currency.USD,
                recipient_details={"account": "ACC-100"},
                description="Initial payout 1",
            ),
            Payout(
                amount="250.50",
                currency=Payout.Currency.EUR,
                recipient_details={"account": "ACC-200"},
                description="Initial payout 2",
            ),
            Payout(
                amount="5000.00",
                currency=Payout.Currency.RUB,
                recipient_details={"account": "ACC-300"},
                description="Initial payout 3",
            ),
        ]
        Payout.objects.bulk_create(payouts)
        self.stdout.write(self.style.SUCCESS("Seeded payouts."))
