from celery import shared_task

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import CustomUser


def generate_email_data(user_id):
    user = CustomUser.objects.get(id=user_id)
    refresh_token = RefreshToken.for_user(user)
    # TODO frontend url from env variales
    frontend_activation_url = f"http://confortdeporvida.cl/account-activation/?token={refresh_token}&user_id={user_id}"
    return {
        "user": user,
        "activation_url": frontend_activation_url,
    }


@shared_task
def send_activation_mail(user_id):
    activation_data = generate_email_data(user_id)

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
        "carlos.w.montecinos@gmail.com",  # TODO get sender from .env
        [activation_data.get("user").email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
