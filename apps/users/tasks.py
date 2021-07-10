from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_mail():
    print("send mail")
    send_mail(
        "title",
        "body",
        "carlos.w.montecinos@gmail.com",
        ["carlos.w.montecinos@gmail.com"],
    )
    return None
