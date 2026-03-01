from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from datetime import date
from .models import ShiftReport
from .serializers import ShiftReportSerializer, ShiftReportCreateSerializer


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'Admin'


class ShiftReportViewSet(viewsets.ModelViewSet):
    queryset = ShiftReport.objects.select_related(
        'caregiver__user',
        'patient__user',
        'payment'
    ).all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ShiftReportCreateSerializer
        return ShiftReportSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        caregiver_id = self.request.query_params.get('caregiver_id')
        if caregiver_id:
            queryset = queryset.filter(caregiver__user_id=caregiver_id)
        
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient__user_id=patient_id)
        
        return queryset.order_by('-start_time')
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def hours_by_caregiver(self, request):
        """
        GET /api/shifts/hours_by_caregiver/?month=2&year=2024
        """
        from apps.caregivers.models import Caregiver
        
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        caregiver_id = request.query_params.get('caregiver_id')
        
        shifts_query = ShiftReport.objects.all()
        
        if year:
            shifts_query = shifts_query.filter(start_time__year=year)
        if month:
            shifts_query = shifts_query.filter(start_time__month=month)
        if caregiver_id:
            shifts_query = shifts_query.filter(caregiver__user_id=caregiver_id)
        
        caregiver_ids = shifts_query.values_list('caregiver__user_id', flat=True).distinct()
        caregivers = Caregiver.objects.filter(user_id__in=caregiver_ids).select_related('user')
        
        results = []
        
        for caregiver in caregivers:
            caregiver_shifts = shifts_query.filter(caregiver=caregiver)
            
            total_hours = caregiver_shifts.aggregate(total=Sum('total_hours'))['total'] or 0
            total_shifts = caregiver_shifts.count()
            
            paid_shifts = caregiver_shifts.filter(payment__isnull=False)
            paid_hours = paid_shifts.aggregate(total=Sum('total_hours'))['total'] or 0
            
            unpaid_hours = float(total_hours) - float(paid_hours)
            hourly_rate = float(caregiver.hourly_rate) if caregiver.hourly_rate else 0
            amount_due = unpaid_hours * hourly_rate
            
            results.append({
                'caregiver_id': caregiver.user_id,
                'caregiver_name': caregiver.user.full_name,
                'caregiver_email': caregiver.user.email,
                'total_hours': float(total_hours),
                'total_shifts': total_shifts,
                'paid_hours': float(paid_hours),
                'unpaid_hours': unpaid_hours,
                'hourly_rate': hourly_rate,
                'amount_due': round(amount_due, 2)
            })
        
        results.sort(key=lambda x: x['unpaid_hours'], reverse=True)
        
        total_all_hours = sum(r['total_hours'] for r in results)
        total_all_unpaid = sum(r['unpaid_hours'] for r in results)
        total_all_amount = sum(r['amount_due'] for r in results)
        
        return Response({
            'period': {'month': int(month) if month else None, 'year': int(year) if year else None},
            'summary': {
                'total_hours': round(total_all_hours, 2),
                'total_unpaid_hours': round(total_all_unpaid, 2),
                'total_amount_due': round(total_all_amount, 2),
                'caregivers_count': len(results)
            },
            'results': results
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def unpaid_hours(self, request):
        """
        GET /api/shifts/unpaid_hours/
        """
        from apps.caregivers.models import Caregiver
        
        unpaid_shifts = ShiftReport.objects.filter(payment__isnull=True).select_related('caregiver__user', 'patient__user')
        
        caregiver_ids = unpaid_shifts.values_list('caregiver__user_id', flat=True).distinct()
        caregivers = Caregiver.objects.filter(user_id__in=caregiver_ids).select_related('user')
        
        results = []
        
        for caregiver in caregivers:
            caregiver_unpaid = unpaid_shifts.filter(caregiver=caregiver)
            
            total_hours = caregiver_unpaid.aggregate(total=Sum('total_hours'))['total'] or 0
            total_shifts = caregiver_unpaid.count()
            
            hourly_rate = float(caregiver.hourly_rate) if caregiver.hourly_rate else 0
            amount_due = float(total_hours) * hourly_rate
            
            results.append({
                'caregiver_id': caregiver.user_id,
                'caregiver_name': caregiver.user.full_name,
                'caregiver_email': caregiver.user.email,
                'bank_account': caregiver.bank_account,
                'hourly_rate': hourly_rate,
                'unpaid_hours': float(total_hours),
                'unpaid_shifts_count': total_shifts,
                'amount_due': round(amount_due, 2)
            })
        
        results.sort(key=lambda x: x['amount_due'], reverse=True)
        
        total_unpaid_hours = sum(r['unpaid_hours'] for r in results)
        total_amount_due = sum(r['amount_due'] for r in results)
        total_shifts = sum(r['unpaid_shifts_count'] for r in results)
        
        return Response({
            'summary': {
                'total_unpaid_hours': round(total_unpaid_hours, 2),
                'total_amount_due': round(total_amount_due, 2),
                'total_unpaid_shifts': total_shifts,
                'caregivers_pending': len(results)
            },
            'results': results
        })