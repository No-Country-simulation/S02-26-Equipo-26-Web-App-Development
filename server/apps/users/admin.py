from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    User, Location, Patient, Caregiver, Admin as AdminProfile,
    Family, Document, Payment, ShiftReport
)


# ========== INLINE ADMINS ==========
class PatientInline(admin.StackedInline):
    """Perfil de paciente inline en User"""
    model = Patient
    can_delete = False
    verbose_name_plural = 'Información de Paciente'
    fk_name = 'user'


class CaregiverInline(admin.StackedInline):
    """Perfil de cuidador inline en User"""
    model = Caregiver
    can_delete = False
    verbose_name_plural = 'Información de Cuidador'
    fk_name = 'user'


class AdminProfileInline(admin.StackedInline):
    """Perfil de admin inline en User"""
    model = AdminProfile
    can_delete = False
    verbose_name_plural = 'Información de Administrador'
    fk_name = 'user'


class DocumentInline(admin.TabularInline):
    """Documentos inline en Caregiver"""
    model = Document
    extra = 0
    fields = ('document_type', 'verification_status', 'upload_date', 'expiry_date')
    readonly_fields = ('upload_date',)


class FamilyInline(admin.TabularInline):
    """Familiares inline en Patient"""
    model = Family
    extra = 1
    fields = ('relationship',)


# ========== LOCATION ADMIN ==========
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'users_count')
    list_filter = ('country',)
    search_fields = ('country', 'city')
    ordering = ('country', 'city')

    def users_count(self, obj):
        """Cantidad de usuarios en esta ubicación"""
        count = User.objects.filter(location=obj).count()
        return format_html(
            '<span style="color: blue; font-weight: bold;">{}</span>',
            count
        )
    users_count.short_description = 'Usuarios'


# ========== CUSTOM USER ADMIN ==========
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'email', 'full_name_colored', 'role_badge', 
        'phone_number', 'is_active_badge', 'created_at'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('email', 'password', 'first_name', 'last_name', 'phone_number')
        }),
        ('Ubicación y Dirección', {
            'fields': ('location', 'address_line')
        }),
        ('Permisos y Rol', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('created_at', 'last_login')
        }),
    )
    
    add_fieldsets = (
        ('Crear Nuevo Usuario', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_active')
        }),
    )
    
    readonly_fields = ('created_at', 'last_login')
    
    # Inlines dinámicos según el rol
    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj:
            if obj.role == 'Patient':
                inlines.append(PatientInline(self.model, self.admin_site))
            elif obj.role == 'Caregiver':
                inlines.append(CaregiverInline(self.model, self.admin_site))
            elif obj.role == 'Admin':
                inlines.append(AdminProfileInline(self.model, self.admin_site))
        return inlines

    def full_name_colored(self, obj):
        """Nombre completo con color según rol"""
        colors = {
            'Admin': '#e74c3c',
            'Caregiver': '#3498db',
            'Patient': '#2ecc71'
        }
        color = colors.get(obj.role, '#95a5a6')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.full_name
        )
    full_name_colored.short_description = 'Nombre Completo'

    def role_badge(self, obj):
        """Badge con el rol del usuario"""
        badges = {
            'Admin': '<span style="background: #e74c3c; color: white; padding: 3px 8px; border-radius: 3px;">👨‍💼 Admin</span>',
            'Caregiver': '<span style="background: #3498db; color: white; padding: 3px 8px; border-radius: 3px;">👨‍⚕️ Cuidador</span>',
            'Patient': '<span style="background: #2ecc71; color: white; padding: 3px 8px; border-radius: 3px;">👤 Paciente</span>'
        }
        return format_html(badges.get(obj.role, ''))
    role_badge.short_description = 'Rol'

    def is_active_badge(self, obj):
        """Badge de estado activo/inactivo"""
        if obj.is_active:
            return format_html(
                '<span style="background: #2ecc71; color: white; padding: 3px 8px; border-radius: 3px;">✓ Activo</span>'
            )
        return format_html(
            '<span style="background: #e74c3c; color: white; padding: 3px 8px; border-radius: 3px;">✗ Inactivo</span>'
        )
    is_active_badge.short_description = 'Estado'


# ========== PATIENT ADMIN ==========
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'get_email', 'get_phone', 'has_medical_history')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    inlines = [FamilyInline]
    
    def user_link(self, obj):
        """Link al usuario"""
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.full_name)
    user_link.short_description = 'Usuario'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_phone(self, obj):
        return obj.user.phone_number or '-'
    get_phone.short_description = 'Teléfono'
    
    def has_medical_history(self, obj):
        if obj.medical_history:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_medical_history.short_description = 'Historia Médica'


# ========== CAREGIVER ADMIN ==========
@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    list_display = (
        'user_link', 'get_email', 'hourly_rate_colored', 
        'verification_badge', 'documents_count'
    )
    list_filter = ('is_verified',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    inlines = [DocumentInline]
    actions = ['verify_caregivers', 'unverify_caregivers']
    
    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.full_name)
    user_link.short_description = 'Usuario'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def hourly_rate_colored(self, obj):
        if obj.hourly_rate:
            return format_html(
                '<span style="color: green; font-weight: bold;">${}</span>',
                obj.hourly_rate
            )
        return '-'
    hourly_rate_colored.short_description = 'Tarifa/Hora'
    
    def verification_badge(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="background: #2ecc71; color: white; padding: 3px 8px; border-radius: 3px;">✓ Verificado</span>'
            )
        return format_html(
            '<span style="background: #e74c3c; color: white; padding: 3px 8px; border-radius: 3px;">✗ No Verificado</span>'
        )
    verification_badge.short_description = 'Verificación'
    
    def documents_count(self, obj):
        count = obj.documents.count()
        approved = obj.documents.filter(verification_status='Approved').count()
        return format_html('{} ({} aprobados)', count, approved)
    documents_count.short_description = 'Documentos'
    
    # Acciones personalizadas
    def verify_caregivers(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} cuidadores verificados.')
    verify_caregivers.short_description = 'Verificar cuidadores seleccionados'
    
    def unverify_caregivers(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} cuidadores desverificados.')
    unverify_caregivers.short_description = 'Desverificar cuidadores seleccionados'


# ========== DOCUMENT ADMIN ==========
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'caregiver_link', 'document_type', 
        'status_badge', 'upload_date', 'expiry_date_colored'
    )
    list_filter = ('document_type', 'verification_status', 'upload_date')
    search_fields = ('caregiver__user__first_name', 'caregiver__user__last_name')
    date_hierarchy = 'upload_date'
    actions = ['approve_documents', 'reject_documents']
    
    fieldsets = (
        ('Información del Documento', {
            'fields': ('caregiver', 'document_type', 'file_url', 'upload_date')
        }),
        ('Verificación', {
            'fields': ('verification_status', 'rejection_reason', 'verified_by')
        }),
        ('Vencimiento', {
            'fields': ('expiry_date',)
        }),
    )
    
    readonly_fields = ('upload_date',)
    
    def caregiver_link(self, obj):
        url = reverse('admin:users_caregiver_change', args=[obj.caregiver.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.caregiver.user.full_name)
    caregiver_link.short_description = 'Cuidador'
    
    def status_badge(self, obj):
        badges = {
            'Pending': '<span style="background: #f39c12; color: white; padding: 3px 8px; border-radius: 3px;">⏳ Pendiente</span>',
            'Approved': '<span style="background: #2ecc71; color: white; padding: 3px 8px; border-radius: 3px;">✓ Aprobado</span>',
            'Rejected': '<span style="background: #e74c3c; color: white; padding: 3px 8px; border-radius: 3px;">✗ Rechazado</span>'
        }
        return format_html(badges.get(obj.verification_status, ''))
    status_badge.short_description = 'Estado'
    
    def expiry_date_colored(self, obj):
        if not obj.expiry_date:
            return '-'
        
        from datetime import date
        days_until_expiry = (obj.expiry_date - date.today()).days
        
        if days_until_expiry < 0:
            color = 'red'
            text = f'Vencido hace {abs(days_until_expiry)} días'
        elif days_until_expiry < 30:
            color = 'orange'
            text = f'Vence en {days_until_expiry} días'
        else:
            color = 'green'
            text = str(obj.expiry_date)
        
        return format_html('<span style="color: {};">{}</span>', color, text)
    expiry_date_colored.short_description = 'Vencimiento'
    
    def approve_documents(self, request, queryset):
        updated = queryset.update(verification_status='Approved', verified_by_id=request.user.id)
        self.message_user(request, f'{updated} documentos aprobados.')
    approve_documents.short_description = 'Aprobar documentos seleccionados'
    
    def reject_documents(self, request, queryset):
        updated = queryset.update(verification_status='Rejected')
        self.message_user(request, f'{updated} documentos rechazados.')
    reject_documents.short_description = 'Rechazar documentos seleccionados'


# ========== PAYMENT ADMIN ==========
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'caregiver_link', 'amount_colored', 
        'status_badge', 'payment_date', 'transaction_id'
    )
    list_filter = ('status', 'payment_date')
    search_fields = ('caregiver__user__first_name', 'caregiver__user__last_name', 'transaction_id')
    date_hierarchy = 'payment_date'
    
    def caregiver_link(self, obj):
        url = reverse('admin:users_caregiver_change', args=[obj.caregiver.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.caregiver.user.full_name)
    caregiver_link.short_description = 'Cuidador'
    
    def amount_colored(self, obj):
        return format_html(
            '<span style="color: green; font-weight: bold; font-size: 14px;">${}</span>',
            obj.amount
        )
    amount_colored.short_description = 'Monto'
    
    def status_badge(self, obj):
        badges = {
            'Pending': '<span style="background: #f39c12; color: white; padding: 3px 8px; border-radius: 3px;">⏳ Pendiente</span>',
            'Success': '<span style="background: #2ecc71; color: white; padding: 3px 8px; border-radius: 3px;">✓ Exitoso</span>',
            'Failed': '<span style="background: #e74c3c; color: white; padding: 3px 8px; border-radius: 3px;">✗ Fallido</span>'
        }
        return format_html(badges.get(obj.status, ''))
    status_badge.short_description = 'Estado'


# ========== SHIFT REPORT ADMIN ==========
@admin.register(ShiftReport)
class ShiftReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'patient_link', 'caregiver_link', 
        'start_time', 'end_time', 'total_hours_colored', 'payment_status'
    )
    list_filter = ('start_time', 'payment__status')
    search_fields = (
        'patient__user__first_name', 'patient__user__last_name',
        'caregiver__user__first_name', 'caregiver__user__last_name'
    )
    date_hierarchy = 'start_time'
    readonly_fields = ('total_hours',)
    
    def patient_link(self, obj):
        url = reverse('admin:users_patient_change', args=[obj.patient.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.patient.user.full_name)
    patient_link.short_description = 'Paciente'
    
    def caregiver_link(self, obj):
        url = reverse('admin:users_caregiver_change', args=[obj.caregiver.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.caregiver.user.full_name)
    caregiver_link.short_description = 'Cuidador'
    
    def total_hours_colored(self, obj):
        if obj.total_hours:
            return format_html(
                '<span style="color: blue; font-weight: bold;">{} hs</span>',
                obj.total_hours
            )
        return '-'
    total_hours_colored.short_description = 'Horas Totales'
    
    def payment_status(self, obj):
        if obj.payment:
            badges = {
                'Pending': '⏳ Pendiente',
                'Success': '✓ Pagado',
                'Failed': '✗ Fallido'
            }
            return badges.get(obj.payment.status, '-')
        return 'Sin pago asignado'
    payment_status.short_description = 'Estado de Pago'


# ========== FAMILY ADMIN ==========
@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_link', 'relationship')
    list_filter = ('relationship',)
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
    
    def patient_link(self, obj):
        url = reverse('admin:users_patient_change', args=[obj.patient.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.patient.user.full_name)
    patient_link.short_description = 'Paciente'


# Personalización del título del admin
admin.site.site_header = "Sistema de Gestión de Cuidadores"
admin.site.site_title = "Admin Cuidadores"
admin.site.index_title = "Panel de Administración"
