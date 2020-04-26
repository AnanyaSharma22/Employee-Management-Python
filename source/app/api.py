from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics, status, exceptions
from oauth2_provider.models import AccessToken
from EmployeeManagement.core.permissions import (PrivateTokenAccessPermission,
                                                 PublicTokenAccessPermission,
                                                 PublicPrivateTokenAccessPermission)
from app.models import Manager, Employee
from app.serializers import (RegisterUserSerializer, LoginUserSerializer, 
                             SignOutUserSerializer, EmployeeSerializer)
from app import message


class SignUpView(generics.CreateAPIView):
    '''
    API for registering new user
    '''
    queryset = Manager.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (PublicTokenAccessPermission, )

class LoginView(generics.CreateAPIView):
    '''
    API for logging in a user
    '''

    queryset = Manager.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = (PublicTokenAccessPermission, )

class SignOutView(generics.UpdateAPIView):
    '''
    API for Expire Access Token to Sign out the User
    '''
    queryset = Manager.objects.all()
    serializer_class = SignOutUserSerializer
    permission_classes = (PrivateTokenAccessPermission, )

    def get_object(self):
        '''
        Get Object
        '''
        token = self.request.META['HTTP_AUTHORIZATION']
        token_type, token = token.split(' ')
        if token:
            try:
                access_token = AccessToken.objects.filter(token=token).get()
            except AccessToken.DoesNotExist:
                return None
        return access_token

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(SignOutView, self).update(request, *args, **kwargs)

class CreateEmployeeView(generics.ListCreateAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (PrivateTokenAccessPermission, )

class UpdateEmployeeView(generics.RetrieveUpdateAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (PrivateTokenAccessPermission, )

    def get_object(self):
        try:
            obj = Employee.objects.get(id=self.kwargs.get('employee_id'))
        except Employee.DoesNotExist:
            raise exceptions.APIException(message.DOES_NOT_EXIST.format("Employee"))
        return obj

    def retrieve(self, *args, **kwargs):
        '''Retrieve'''
        try:
            return super(UpdateEmployeeView, self).retrieve(*args, **kwargs)
        except (Http404, Employee.DoesNotExist):
            return Response({MESSAGE: message.EMPLOYEE_NOT_FOUND}, status=settings.HTTP_API_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            return super(UpdateEmployeeView,self).patch(request, *args, **kwargs)
        except Brand.DoesNotExist:
            return Response({MESSAGE: message.EMPLOYEE_NOT_FOUND}, status=settings.HTTP_API_ERROR)
        return Response()
        
    
