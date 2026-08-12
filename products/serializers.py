from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "created_at",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater that 0"
            )

        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Quantity cannot be negative"
            )

        return value

    def validate(self, data):
        if data["quantity"] == 0 and data["price"] > 100000:
            raise serializers.ValidationError(
                "A product with zero quantity cannot have a price above 100000"
            )

        return data