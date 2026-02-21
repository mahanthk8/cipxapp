from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('OFFICER', 'Officer'),
        ('USER', 'User'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    p_user = models.BooleanField(default=False)  # influential citizen
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    star = models.FloatField(default=1)


    def __str__(self):
        return f"{self.username} ({self.role})"
