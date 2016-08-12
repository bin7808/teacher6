import re
from django.db import models
from django.forms import ValidationError
from .validators import phone_number_validator


class PhoneNumberField(models.CharField):
    default_validators = [phone_number_validator]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)

