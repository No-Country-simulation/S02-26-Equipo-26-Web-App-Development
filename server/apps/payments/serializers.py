from rest_framework import serializers
from .models import Payment
from apps.caregivers.models import Caregiver


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer completo para pagos.
    """
    caregiver_id = serializers.IntegerField(source='caregiver.user_id', read_only=True)
    caregiver_name = serializers.CharField(source='caregiver.user.full_name', read_only=True)
    caregiver_email = serializers.CharField(source='caregiver.user.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'caregiver_id',
            'caregiver_name',
            'caregiver_email',
            'period_start',
            'period_end',
            'total_amount',
            'transaction_id',
            'status',
            'payment_date'
        ]
        read_only_fields = ['id']


class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear pagos.
    """
    caregiver_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'caregiver_id',
            'period_start',
            'period_end',
            'total_amount',
            'transaction_id',
            'status',
            'payment_date'
        ]
    
    def validate(self, data):
        # Verificar que el cuidador existe
        try:
            caregiver = Caregiver.objects.get(user_id=data['caregiver_id'])
            data['caregiver'] = caregiver
        except Caregiver.DoesNotExist:
            raise serializers.ValidationError({
                'caregiver_id': 'Cuidador no encontrado'
            })
        
        # Validar que period_end >= period_start
        if data['period_end'] < data['period_start']:
            raise serializers.ValidationError({
                'period_end': 'period_end debe ser posterior o igual a period_start'
            })
        
        return data
    
    def create(self, validated_data):
        caregiver = validated_data.pop('caregiver')
        validated_data.pop('caregiver_id', None)
        
        payment = Payment.objects.create(
            caregiver=caregiver,
            **validated_data
        )
        return payment