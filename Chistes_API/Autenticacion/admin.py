from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.admin.sites import AdminSite

#from .forms import OTPAuthenticationFormMixin


def _admin_template_for_django_version():
    return 'otp/admin111/login.html'


class OTPAdminAuthenticationForm(AdminAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.Select)
    otp_token = forms.CharField(required=False)

    otp_challenge = forms.CharField(required=False)

    def clean(self):
        self.cleaned_data = super().clean()
        self.clean_otp(self.get_user())

        return self.cleaned_data



class OTPAdminSite(AdminSite):
    name = 'otpadmin'

    login_form = OTPAdminAuthenticationForm

    login_template = _admin_template_for_django_version()

    def __init__(self, name='otpadmin'):
        super().__init__(name)

    def has_permission(self, request):
        return super().has_permission(request) and request.user.is_verified()