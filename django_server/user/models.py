from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from share.models import TimeModel

class CompanyIndexModel(models.Model):
    name = models.CharField(
        max_length=25
    )
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, TimeModel):
    email = models.EmailField(
        unique=True
    )
    name = models.CharField(
        max_length=10
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    companyFK = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'  # 기본 id로 이메일을 사용
    REQUIRED_FIELDS = ['name']  # 필수 입력 필드

    def __str__(self):
        return self.email