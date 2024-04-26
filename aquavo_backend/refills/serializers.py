from rest_framework import serializers
from .models import Refill
from accounts.models import CustomUser
from accounts.serializers import CustomerSerializer

class RefillSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Refill
        fields = ['id', 'customer', 'amount_liters', 'amount_money', 'created_at']
