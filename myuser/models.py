from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator


class MyUserManager(BaseUserManager):
    def create_user(self, phone, email, id, first_name, last_name, password=None):
        if not phone:
            raise ValueError("you have import phone number")
        if not id:
            raise ValueError("you have import id")
        if not first_name:
            raise ValueError("you have import first name")
        if not email:
            raise ValueError("you have import email")

        user = self.model(
            email=self.normalize_email(email),
            id=id,
            first_name=first_name,
            phone=phone,
            last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, id, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            id=id,
            first_name=first_name,
            phone=phone,
            last_name=last_name
        )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True,
                             validators=[
                                 RegexValidator(
                                     regex="\A(09)(0|1|2|3|9)[0-9]{7}\d\Z", message="error phone number")
                             ])
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['id', 'phone', 'first_name', 'email']

    objects = MyUserManager()

    def __str__(self):
        return self.id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
