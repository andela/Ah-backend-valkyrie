import jwt

from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView,
    GenericAPIView
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .renderers import UserJSONRenderer
from .backends import JWTAuthentication
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from authors.apps.core.email_handler import email_template
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from django.conf import settings


class RegistrationAPIView(GenericAPIView):
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
        # Send verification Email to registered user
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
        <p>Thank you for registering with Author\'s Haven. \
        Please follow the link below to activate your account.</p> \
        <br> {}'.format((user.username).capitalize(), url)

        return email_template(subject, content, user.email)


class UsersListAPIView(ListAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAccountVerificationAPIView(GenericAPIView):
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


class UsersListAPIView(ListAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginAPIView(GenericAPIView):
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
    queryset = User.objects.all()
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        user = User.objects.get(id=kwargs.get('pk'))
        if self.request.user.id != self.kwargs.get("pk"):
            raise PermissionDenied("You are not allowed perform this action")

        serializer_data = {
            'username': user_data.get('username', user.username),
            'email': user_data.get('email', user.email),

            'profile': {
                'first_name': user_data.get('first_name', request.user.profile.first_name),
                'last_name': user_data.get('last_name', request.user.profile.last_name),
                'country': user_data.get('country', request.user.profile.country),
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image)
            }
        }

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPasswordResetRequestAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        """reset password email template"""
        email = request.data.get('email')
        protocol = 'https://' if request.is_secure() else 'http://'
        current_site = get_current_site(request)

        if not email:
            message = {'message': 'An email address is required'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        user = User.fetch_user(email)

        if not user:
            message = {
                'message': 'User with email {} doesnot exist'.format(email)}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        # Ensure that you send a reset mail to a valid user
        token = JWTAuthentication.generate_password_reset_token(email)

        reset_url = protocol + current_site.domain + reverse(
            'reset_password_confirm',
            kwargs={"token": token}
        )
        subject, to = ('Valkyrie-Authors-Haven Password Reset', email)

        html_content = "<p>Click on this <a href='" + \
            reset_url + "'>Link<a> to reset your password</p> " + reset_url

        email_template(subject, html_content, to)

        return Response(
            {
                "message":
                "A password reset email has been sent to your email account!"},
            status=status.HTTP_200_OK)


class UserPasswordResetConfirmAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def put(self, request, token):
        """update user password"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except Exception as error:
            return Response(
                {'message': str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.fetch_user(payload['email'])
        password = request.data.get('password')

        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user.set_password(password)
        user.save()

        return Response(
            {"message": "Password reset successful!"},
            status=status.HTTP_200_OK)
