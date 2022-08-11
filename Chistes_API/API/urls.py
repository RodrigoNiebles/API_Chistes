from django.urls import path
from .views import ChistesView
from rest_framework.urlpatterns import format_suffix_patterns
from API import views
from rest_framework.views import APIView
from API.views import chistes_Chuck

urlpatterns = [
    path ('Chuck/<int:pk>',views.chistes_Chuck),
    path ('chiste/<int:pk>', ChistesView.as_view(), name='chiste')
]   