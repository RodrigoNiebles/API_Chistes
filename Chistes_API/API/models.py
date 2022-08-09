from django.db import models
from django.db.models import Model

class Chistes(models.Model):
    categories = []
    created_at = models.DateField(auto_now=True, null=True, blank=False)
    icon_url = models.URLField(max_length=200)
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=False)
    url = models.URLField(max_length=200)
    value = models.CharField(max_length=1000)


