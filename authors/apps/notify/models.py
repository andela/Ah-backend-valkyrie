from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class MailList(models.Model):
    """
    database table that stores all
    users that subscribe to recieve notifications
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recieve_email_notifications = models.BooleanField(default=True)
    recieve_push_notifications = models.BooleanField(default=True)

    @classmethod
    def did_subscribe_for_email_notifications(cls, user):
        """
        check if a particular user is
        subscribed to recieve email notifications
        """
        result = MailList.objects.get_or_create(user=user)
        return result[0].recieve_email_notifications

    @classmethod
    def did_subscribe_for_push_notifications(cls, user):
        """
        check if a particular user is
        subscribed to recieve email notifications
        """
        result = MailList.objects.get_or_create(user=user)
        return result[0].recieve_push_notifications
