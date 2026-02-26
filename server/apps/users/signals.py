from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Admin as AdminProfile
from apps.patients.models import Patient
from apps.caregivers.models import Caregiver
from apps.documents.models import Document
from apps.payments.models import Payment


# ========== SIGNAL: Crear perfil automáticamente al crear usuario ==========
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cuando se crea un usuario, automáticamente se crea su perfil
    según el rol (Patient, Caregiver, Admin)
    """
    if created:
        if instance.role == 'Patient':
            Patient.objects.get_or_create(user=instance)
            print(f"✅ Perfil de Paciente creado para {instance.email}")
        
        elif instance.role == 'Caregiver':
            Caregiver.objects.get_or_create(user=instance)
            print(f"✅ Perfil de Cuidador creado para {instance.email}")
        
        elif instance.role == 'Admin':
            AdminProfile.objects.get_or_create(user=instance)
            print(f"✅ Perfil de Admin creado para {instance.email}")


# ========== SIGNAL: Enviar email de bienvenida ==========
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Envía un email de bienvenida cuando se registra un nuevo usuario
    """
    if created:
        try:
            subject = f'Bienvenido a nuestra plataforma, {instance.first_name}!'
            message = f'''
            Hola {instance.full_name},
            
            ¡Bienvenido a nuestro sistema de gestión de cuidadores!
            
            Tu cuenta ha sido creada exitosamente con el rol de: {instance.get_role_display()}
            
            Puedes iniciar sesión con tu email: {instance.email}
            
            Saludos,
            El equipo de Cuidadores
            '''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=True,  # No falla si el email no se envía
            )
            print(f"📧 Email de bienvenida enviado a {instance.email}")
        except Exception as e:
            print(f"❌ Error al enviar email: {str(e)}")


# ========== SIGNAL: Notificar cuando se verifica un cuidador ==========
@receiver(post_save, sender=Caregiver)
def notify_caregiver_verification(sender, instance, created, **kwargs):
    """
    Notifica al cuidador cuando su perfil es verificado
    """
    if not created:  # Solo si es una actualización
        if instance.is_verified:
            try:
                subject = '¡Tu perfil ha sido verificado!'
                message = f'''
                Hola {instance.user.full_name},
                
                ¡Buenas noticias! Tu perfil de cuidador ha sido verificado.
                
                Ya puedes comenzar a trabajar y recibir asignaciones.
                
                Saludos,
                El equipo de Cuidadores
                '''
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [instance.user.email],
                    fail_silently=True,
                )
                print(f"✅ Notificación de verificación enviada a {instance.user.email}")
            except Exception as e:
                print(f"❌ Error al enviar notificación: {str(e)}")


# ========== SIGNAL: Notificar cambio de estado de documento ==========
@receiver(post_save, sender=Document)
def notify_document_status_change(sender, instance, created, **kwargs):
    """
    Notifica al cuidador cuando cambia el estado de un documento
    """
    if not created:  # Solo en actualizaciones
        if instance.verification_status == 'Approved':
            subject = 'Documento Aprobado'
            message = f'''
            Hola {instance.caregiver.user.full_name},
            
            Tu documento de tipo "{instance.get_document_type_display()}" ha sido APROBADO.
            
            Gracias por tu colaboración.
            '''
        elif instance.verification_status == 'Rejected':
            subject = 'Documento Rechazado'
            message = f'''
            Hola {instance.caregiver.user.full_name},
            
            Lamentamos informarte que tu documento de tipo "{instance.get_document_type_display()}" ha sido RECHAZADO.
            
            Motivo: {instance.rejection_reason or 'No especificado'}
            
            Por favor, sube un nuevo documento corregido.
            '''
        else:
            return  # No enviar email si está pendiente
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.caregiver.user.email],
                fail_silently=True,
            )
            print(f"📄 Notificación de documento enviada a {instance.caregiver.user.email}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")


# ========== SIGNAL: Notificar pago exitoso ==========
@receiver(post_save, sender=Payment)
def notify_payment_success(sender, instance, created, **kwargs):
    """
    Notifica al cuidador cuando recibe un pago
    """
    if not created and instance.status == 'Success':
        try:
            subject = f'Pago Recibido - ${instance.amount}'
            message = f'''
            Hola {instance.caregiver.user.full_name},
            
            ¡Has recibido un pago!
            
            Monto: ${instance.amount}
            Fecha: {instance.payment_date}
            ID de Transacción: {instance.transaction_id}
            
            El dinero debería reflejarse en tu cuenta bancaria en las próximas 24-48 horas.
            
            Saludos,
            El equipo de Cuidadores
            '''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.caregiver.user.email],
                fail_silently=True,
            )
            print(f"💰 Notificación de pago enviada a {instance.caregiver.user.email}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")


# ========== SIGNAL: Logging de cambios en usuarios ==========
@receiver(pre_save, sender=User)
def log_user_changes(sender, instance, **kwargs):
    """
    Registra cambios importantes en el modelo User
    """
    if instance.pk:  # Si el usuario ya existe
        try:
            old_instance = User.objects.get(pk=instance.pk)
            
            # Detectar si el usuario fue desactivado
            if old_instance.is_active and not instance.is_active:
                print(f"⚠️ Usuario {instance.email} ha sido DESACTIVADO")
            
            # Detectar si cambió el rol
            if old_instance.role != instance.role:
                print(f"🔄 Usuario {instance.email} cambió de rol: {old_instance.role} → {instance.role}")
                
        except User.DoesNotExist:
            pass
