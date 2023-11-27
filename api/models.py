from django.db import models
from django.contrib.auth.hashers import make_password

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=False)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField(default=0)
    is_active = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add = True)

    class Meta:
        managed = False
        db_table = 'auth_user'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Sms(models.Model):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    auth_number = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms'

    @classmethod
    def create_sms(cls, phone_number, auth_number):
        sms = cls(phone_number=phone_number, auth_number=auth_number)
        sms.save()