from django.contrib import admin, messages as flash_messages
from app.models import Manager, Employee
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.auth.forms import (AdminPasswordChangeForm,
                                       UserChangeForm)
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.conf.urls import url

# Register your models here.

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())
class CustomUserAdmin(admin.ModelAdmin):
    """
    Custom Admin class for Custom user model
    """

    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('firstname', 'lastname', 'address', 'company')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                      'is_app_user', 'is_active')}),
    )

    list_display = ['email', 'firstname', 'lastname', 'address', 'company', 'is_active']

    actions = ['make_active', 'make_inactive', ]
    search_fields = ['email', 'firstname', 'lastname']

class EmployeeAdmin(admin.ModelAdmin):
    """
    Custom Admin class for Employee model
    """
    def __init__(self, *args, **kwargs):
        super(EmployeeAdmin, self).__init__(*args, **kwargs)

    # fieldsets = (
    #     (None, {'fields': ('email', '')}),
    #     ('Personal info', {
    #         'fields': ('firstname', 'lastname', 'address', 'dob', 'city')}),
    #     ('Permissions', {'fields': ('is_active')}),
    # )

    list_display = ['firstname', 'lastname', 'address', 'city', 'is_active']

    search_fields = ['firstname', 'lastname']


admin.site.register(Manager, CustomUserAdmin)
admin.site.register(Employee, EmployeeAdmin)