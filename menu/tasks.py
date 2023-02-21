from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Dish
from django.utils import timezone
from datetime import timedelta


User = get_user_model()


@shared_task()
def mail():
    date = timezone.now() - timedelta(days=1)
    new_dishes = Dish.objects.filter(last_modification__gt=date)
    if new_dishes:
        users = User.objects.all()
        recipient_list = [user.email for user in users]
        subject = "Nowe dania"
        message = f"Nowe dania!"
        for dish in new_dishes:
            message += f"\n Nazwa - {dish.name}, opis - {dish.description}, cena - {dish.price}, " \
                       f"czas przygotowania {dish.preparation_time}, wegetariańskie - {dish.is_vegetarian}"
        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list)

