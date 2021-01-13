"""
Definition of models.
"""

from django.db import models
class UserForm(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username

# Create your models here.
