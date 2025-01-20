from celery import shared_task
from .models import Notification

@shared_task
def delete_viewed_notifications(user_id):
    Notification.objects.filter(user_id=user_id, viewed=True).delete()
