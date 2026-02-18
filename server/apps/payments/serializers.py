from rest_framework import serializers
from apps.users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    caregiver_email = serializers.CharField(source='caregiver.user.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'caregiver', 'caregiver_name', 'caregiver_email',
            'amount', 'transaction_id', 'status', 'payment_date'
        ]
        read_only_fields = ['id']