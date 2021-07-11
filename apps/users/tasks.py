from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from rest_framework_simplejwt.tokens import RefreshToken


from apps.users.models import CustomUser


def generate_activation_email_data(user_id):
    user = CustomUser.objects.get(id=user_id)
    refresh_token = RefreshToken.for_user(user)
    activation_url = settings.ACCOUNT_ACTIVATION_URL
    frontend_activation_url = (
        f"{activation_url}?token={refresh_token}&user_id={user_id}"
    )
    return {
        "user": user,
        "activation_url": frontend_activation_url,
    }


@shared_task
def send_activation_email(user_id):
    activation_data = generate_activation_email_data(user_id)

    text_template = get_template("email/activation_email.txt")
    html_template = get_template("email/activation_email.html")

    email_context = {
        "email_data": activation_data,
    }

    text_message = text_template.render(email_context)
    html_message = html_template.render(email_context)

    email = EmailMultiAlternatives(
        "Estas a un paso de Ganar!",
        text_message,
        settings.EMAIL_HOST_USER,
        [activation_data.get("user").email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
