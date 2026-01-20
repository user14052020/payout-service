from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from payouts.models import Payout


class PayoutAPITests(APITestCase):
    def test_create_payout_success(self):
        payload = {
            "amount": "100.00",
            "currency": "USD",
            "recipient_details": {"account": "ACC-123"},
            "description": "Test payout",
        }

        with patch("payouts.tasks.process_payout.delay") as mocked_delay:
            response = self.client.post("/api/v1/payouts/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Payout.Status.PENDING)
        mocked_delay.assert_called_once()

    def test_create_payout_triggers_celery(self):
        payload = {
            "amount": "50.00",
            "currency": "EUR",
            "recipient_details": {"account": "ACC-999"},
            "description": "Trigger",
        }

        with patch("payouts.tasks.process_payout.delay") as mocked_delay:
            response = self.client.post("/api/v1/payouts/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mocked_delay.assert_called_once()
