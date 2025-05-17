from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=255, default="")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class Resume(models.Model):
    full_name = models.CharField(max_length=255, default="")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return f"Resume {self.id} - {self.full_name}"


class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
