from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .backends import JWTAuthentication
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from authors.apps.core.email_handler import email_template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens  import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from .models import User


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        self.send_verification_email(data, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def send_verification_email(self, user, request):
        #Send verification Email to registered user
        token = default_token_generator.make_token(user)
        encoded_email = urlsafe_base64_encode(
            force_bytes(user.email)
        ).decode('utf-8')
        protocol = 'https://' if request.is_secure() else 'http://'
        domail = '{}{}'.format(protocol, get_current_site(request))
        url = '{}{}'.format(
            domail,
            reverse(
                'user-account-verification', args=(token, encoded_email,)
            )
        )
        subject = 'Author\'s Haven Account Verification.'
        content = '<p><strong>Hello {}!</strong> </p> \
        <p>Thank you for registering with Authors Haven. \
        Please follow the link below to activate your account.</p> \
        <br> {}'.format((user.username).capitalize(), url)
        
        return email_template(subject, content, user.email)


class UserAccountVerificationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def get(self, request, token, email):
        decoded_email = force_text(urlsafe_base64_decode(email))
        try:
            user = User.objects.get(email=decoded_email)
            verify_token = default_token_generator.check_token(user, token)
            if verify_token:
                response = 'Your account is already verified.'
                if user.is_active == False:
                    response = 'Your account has been verified successfully.'
                    user.is_active = True
                    user.save()
                return Response(
                    data={'message': response}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={'message': 'Invalid Token used.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                data={
                    'message': 'Cannot find this user'
                }, status=status.HTTP_404_NOT_FOUND
            )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
