from dataclasses import field, fields
from rest_framework import serializers
from API.models import Chistes

class ChisteSerializer (serializers.ModelSerializer):
    class Meta:
        model = Chistes
        fields = '__all__'