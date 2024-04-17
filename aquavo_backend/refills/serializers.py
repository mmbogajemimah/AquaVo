from rest_framework import serializers
from .models import Refill

class RefillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refill
        fields = ['id', 'customer', 'amount_liters', 'amount_money', 'created_at']
        