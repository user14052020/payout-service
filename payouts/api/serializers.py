from decimal import Decimal

from rest_framework import serializers

from payouts.models import Payout


class PayoutReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = [
            "id",
            "amount",
            "currency",
            "recipient_details",
            "status",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_amount(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value

    def validate_recipient_details(self, value: dict) -> dict:
        if not isinstance(value, dict):
            raise serializers.ValidationError("Recipient details must be an object.")
        if not value.get("account"):
            raise serializers.ValidationError("Recipient details must include 'account'.")
        return value

    def validate_description(self, value: str) -> str:
        if value and len(value) > 1024:
            raise serializers.ValidationError("Description is too long.")
        return value


class PayoutCreateSerializer(PayoutReadSerializer):
    class Meta(PayoutReadSerializer.Meta):
        read_only_fields = ["id", "status", "created_at", "updated_at"]


class PayoutUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ["status", "description"]
