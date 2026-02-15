from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    caregiver_email = serializers.CharField(source='caregiver.caregiver.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'payment_id', 'caregiver', 'caregiver_email', 'amount',
            'transaction_id', 'status', 'payment_date'
        ]