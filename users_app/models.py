from django.core.exceptions import ValidationError

from django.db import models
import re


def validate_phone_number(value):
    if not re.match(r'^[\d+\-()\s]+$', value):
        raise ValidationError(
            'Die Telefonnummer darf nur Zahlen, Leerzeichen, "+", "-", oder "()" enthalten.')


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15, validators=[validate_phone_number])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
