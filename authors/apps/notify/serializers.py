from rest_framework import serializers

from authors.apps.authentication.serializers import UserSerializer
from authors.apps.notify.models import MailList


class FetchMailListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MailList
        fields = ('user', 'recieve_email_notifications',
                  'recieve_push_notifications')


class CreateMailListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MailList
        fields = '__all__'
