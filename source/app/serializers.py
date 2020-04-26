from django.conf import settings
from django.forms import model_to_dict
from django.utils import timezone
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from app.models import Manager, Employee
from .utils import UserAccessToken
from oauth2_provider.models import AccessToken
from app import message
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    '''
    serializer for user
    '''
    class Meta:
        '''
        meta for user
        '''
        model = get_user_model()
        fields = "__all__"
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

class RegisterUserSerializer(UserSerializer):

    access_token = serializers.SerializerMethodField('get_user_access_token')                                      

    def __init__(self, *args, **kwargs):
        super(RegisterUserSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        self.accesst_token = None

        if context:
            self.request = kwargs['context']['request']

    class Meta:
        model = get_user_model()
        fields = "__all__"
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def validate_email(self, email_value):
        '''validate email'''
        try:
            get_user_model().objects.filter(email__iexact=email_value).get()
            # Log an error message
            logger.error('User already exist !')
            raise ValidationError("User already exist !")
        except get_user_model().DoesNotExist:
            return email_value

    def create(self, validated_data):
        ''' create access token '''
        validated_data['is_active'] = True
        instance = get_user_model().objects.create(**validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        self.accesst_token = self.create_auth_token(instance)
        return instance

    def create_auth_token(self, instance):
        '''create auth token '''
        token_application_name = settings.APPLICATION_NAME
        user_access_token = UserAccessToken(
            self.request, instance, token_application_name)
        access_token = user_access_token.create_oauth_token()
        return access_token

    def get_user_access_token(self, user):
        '''get user access token '''
        return self.accesst_token.token

class LoginUserSerializer(UserSerializer):
    email = serializers.EmailField(required=True)
    access_token = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True)

    class Meta:
        '''meta information for login user serializer'''
        model = get_user_model()
        fields = ('email', 'access_token', 'is_active',
                   'password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def __init__(self, *args, **kwargs):
        super(LoginUserSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        self.access_token = None
        self.user = None
        self.error_message = None
        if context:
            self.request = kwargs['context']['request']

    def authenticate(self, email, password):
        """
        authenticate user with provided crednetials
        """
        data = None
        try:
            user = get_user_model().objects.filter(email__iexact=email).get()
            if not user.is_active:
                raise ValidationError(message.USER_ACCOUNT_NOT_ACTIVE)
            elif user.check_password(password):
                data = user
        except get_user_model().DoesNotExist:
            data = None
        return data

    def validate(self, validated_data):
        '''validating email'''
        self.user = self.authenticate(validated_data['email'], validated_data['password'])
        if self.user is None:
            raise ValidationError(message.LOGIN_AUTHENTICATION_INVALID)
        return validated_data

    def create(self, validated_data):
        token_application_name = settings.APPLICATION_NAME
        user_access_token = UserAccessToken(self.request, self.user, token_application_name)
        access_token = user_access_token.create_oauth_token()
        self.access_token = access_token.token
        return self
    
    @property
    def data(self):
        user = model_to_dict(self.user)
        user.pop('is_app_user')
        user.pop('password')
        user.pop('user_permissions')
        user.pop('is_superuser')
        user.pop('is_staff')
        user.pop('last_login')
        user.pop('is_active')
        user['access_token'] = self.access_token
        return {'message': message.USER_LOGGEDIN_SUCCESSFULLY, 'extras': user}

class SignOutUserSerializer(serializers.ModelSerializer):
    '''serializer for user sign out'''

    class Meta:
        '''meta information for sign out user'''
        model = AccessToken
        fields = ('token', )
        extra_kwargs = {
            'token': {
                'write_only': True,
            }
        }

    def update(self, *args, **kwargs):
        self.instance.expires = timezone.now()
        self.instance.save()
        return self.instance

    def to_representation(self, *args, **kwargs):
        return {
            'message': message.LOGGED_OUT
        }

class EmployeeSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(EmployeeSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)

        if context:
            self.request = kwargs['context']['request']

    class Meta:
        '''meta information for create employee serializer'''
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        ''' create employee '''
        validated_data['is_active'] = True
        instance = Employee.objects.create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super(EmployeeSerializer, self).update(instance, validated_data)
        return instance
    
