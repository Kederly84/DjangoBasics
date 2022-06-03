from celery import shared_task
from django.core.mail import send_mail

import local_settings
from authapp.models import User


@shared_task
def send_feedback_mail(message_body: str, message_from: int = None) -> None:
    if message_from is not None:
        user_from = User.objects.filter(pk=message_from).first().get_full_name()
    else:
        user_from = 'Аноним'

    send_mail(
        subject=f'Feedback from: {user_from}',
        message=message_body,
        recipient_list=['amaksimov744@gmail.com'],
        from_email=local_settings.EMAIL_HOST_USER,
        fail_silently=False
    )
