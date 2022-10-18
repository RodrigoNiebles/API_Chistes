"""Chistes_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
from django.contrib import admin
from django.urls import path, include



#from django_otp.admin import OTPAdminSite
#admin.site.__class__ = OTPAdminSite

#class OTPAdmin(OTPAdminSite):
#    pass 

#from django.contrib.auth.models import User
#from django_otp.plugins.otp_totp.models import TOTPDevice

#admin_site = OTPAdmin(name='OTPAdmin')
#admin_site.register(User)
#admin_site.register(TOTPDevice)



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/', admin_site.urls),
    path('', include('API.urls')),
]
"""






from django.urls import path, include
from django.contrib import admin

from django_otp.admin import OTPAdmin, AdminSite



'''
class TestAdminSite(admin.AdminSite):
    """test admin site."""

    login_form = AdminSite.login_form
    login_template = AdminSite.login_template

    def __init__(self, *args, **kwargs):
        """Init."""
        super(TestAdminSite, self).__init__(*args, **kwargs)
        self._registry = admin.site._registry.copy()
'''

OTPAdmin.enable()
admin.site = AdminSite()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr/', include("django_otp.urls")),
    path('', include('API.urls')),
]