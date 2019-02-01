from smtplib import SMTPException

import notifications
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from notifications.models import Notification
from notifications.signals import notify
from authors.apps.notify.models import MailList


class Notifier:
    @classmethod
    def batch_follower_email_notifier(cls, author, followers, **kwargs):
        """
        send email notifications to recipients
        """
        subject = 'New Article Notification'
        message = """
        {} has published a new article.
        You are recieving this email because you are subscribed to email notifications.
        To unsubscribe from recieving emails, login and follow the provided instructions.
        """.format(author.username)

        for follower in followers:
            notification = None
            # check if user/recipient subscribed for push notifications
            if MailList.did_subscribe_for_push_notifications(follower.user):
                try:
                    notification = Notification.objects.latest(
                        'timestamp',)

                except Exception:
                    notification = Notification.objects.create(
                        actor=author, recipient=follower.user,
                        verb=subject)
                try:
                    notify.send(
                        sender=author, recipient=follower.user,
                        verb=subject, **kwargs
                    )
                except Exception:
                    raise Exception("Notification sending failed!")

            cls.email_notification(
                follower.user, notification, subject=subject, message=message)

    @classmethod
    def email_notification(cls, user, notification, **kwargs):
        """user email notifications"""
        subject = kwargs.get('subject', 'Authors-Haven-Email-Notification')
        message = kwargs.get('message', '')

        if cls.is_valid_user(user):
            if MailList.did_subscribe_for_email_notifications(user):
                try:
                    email = EmailMessage(
                        subject=subject, body=message, to=[user.email]
                    )
                    email.content_subtype = 'html'
                    email.send()
                    # mark notification as sent
                    notification.emailed = True
                    notification.save()

                except SMTPException as e:
                    return {'message': str(e)}

    @classmethod
    def fetch_unread_notifications(cls, user):
        if cls.is_valid_user(user):
            return user.notifications.unread()

    @classmethod
    def fetch_read_notifications(cls, user):
        if cls.is_valid_user(user):
            return user.notifications.read()

    @classmethod
    def fetch_all_notifications(cls, user):
        if cls.is_valid_user(user):
            return user.notifications.all()

    @classmethod
    def is_valid_user(cls, user):
        if not isinstance(user, get_user_model()):
            raise TypeError(
                f"{user} is not a valid {get_user_model()} model"
            )
        return True
