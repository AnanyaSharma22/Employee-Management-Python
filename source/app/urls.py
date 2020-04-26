from django.conf.urls import url
from app.api import (SignUpView, LoginView, SignOutView, CreateEmployeeView, UpdateEmployeeView)

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name="signup-user"),
    url(r'^login/$', LoginView.as_view(), name="login-user"),
    url(r'^logout/$', SignOutView.as_view(), name="logout-user"),
    url(r'^employee/$', CreateEmployeeView.as_view(), name="create-employee"),
    url(r'^employee/(?P<employee_id>.+)/$', UpdateEmployeeView.as_view(), name="edit_employee"),
]