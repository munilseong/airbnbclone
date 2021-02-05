from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICE = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_KOREAN = "kr"
    LANGUAGE_ENGLISH = "en"
    LANGUAGE_CHOICE = ((LANGUAGE_KOREAN, "Korean"), (LANGUAGE_ENGLISH, "English"))

    CURRENCY_KRW = "krw"
    CURRENCY_USD = "usd"
    CURRENCY_CHOICE = ((CURRENCY_KRW, "KRW"), (CURRENCY_USD, "USD"))
    gender = models.CharField(
        choices=GENDER_CHOICE, max_length=10, null=True, blank=True
    )
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    bio = models.TextField(default="", blank=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICE,
        max_length=2,
        null=True,
        blank=True,
        default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICE,
        max_length=3,
        null=True,
        blank=True,
        default=CURRENCY_KRW,
    )
    birthdate = models.DateField(null=True)
    superhost = models.BooleanField(default=False)