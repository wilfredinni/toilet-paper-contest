from celery import shared_task

from django.core.mail import send_mail

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import CustomUser


def generate_email_data(user_id):
    user = CustomUser.objects.get(id=user_id)
    refresh_token = RefreshToken.for_user(user)
    # TODO frontend url from env variales
    frontend_activation_url = f"http://confortdeporvida.cl/account-activation/?token={refresh_token}&user_id={user_id}"
    return {
        "user_id": user.id,
        "username": user.username,
        "user_email": user.email,
        "activation_url": frontend_activation_url,
    }
    # return {
    #     "subject": "Welcome to the site",
    #     "message": "You have successfully registered to our site",
    #     "from_email": "carlos.w.montecinos@gmail.com",
    #     "recipient_list": ["carlos.w.montecinos@gmail.com"],
    # }


@shared_task
def send_activation_mail(user_id):
    data = generate_email_data(user_id)
    send_mail(
        "title",
        data.get("activation_url"),
        "carlos.w.montecinos@gmail.com",
        [data.get("user_email")],
    )
    return None
