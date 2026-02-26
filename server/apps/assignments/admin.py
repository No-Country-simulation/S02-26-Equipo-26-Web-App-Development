from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'caregiver_link',
        'patient_link',
        'start_date',
        'end_date',
        'care_type',
        'status_badge',
        'created_at'
    )
    list_filter = ('status', 'care_type', 'start_date')
    search_fields = (
        'caregiver__user__first_name',
        'caregiver__user__last_name',
        'patient__user__first_name',
        'patient__user__last_name'
    )
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    
    fieldsets = (
        ('Asignación', {
            'fields': ('caregiver', 'patient', 'assigned_by')
        }),
        ('Periodo', {
            'fields': ('start_date', 'end_date')
        }),
        ('Detalles', {
            'fields': ('care_type', 'status')
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def caregiver_link(self, obj):
        url = reverse('admin:users_caregiver_change', args=[obj.caregiver.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.caregiver.user.full_name)
    caregiver_link.short_description = 'Cuidador'
    
    def patient_link(self, obj):
        url = reverse('admin:users_patient_change', args=[obj.patient.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.patient.user.full_name)
    patient_link.short_description = 'Paciente'
    
    def status_badge(self, obj):
        colors = {
            'Active': '#2ecc71',
            'Completed': '#95a5a6',
            'Cancelled': '#e74c3c',
            'OnHold': '#f39c12'
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Estado'