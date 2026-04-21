from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


# ✅ USER MANAGER
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')

        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)


# ✅ USER MODEL
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    role_choice = (
        ('admin', 'admin'),
        ('user', 'user'),
        ('servicestaff', 'servicestaff'),
    )
    role = models.CharField(max_length=100, choices=role_choice, default='user')

    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
      # 🔴 ADD THIS AT TOP


    # 👇 INSIDE User MODEL (replace old field)
    phoneNumber = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    # ✅ LOGIN FIELD
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# ✅ ADMIN MODEL
class Admin(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    admin_level = models.CharField(max_length=50)

    class Meta:
        db_table = "Admin"

    def __str__(self):
        return self.userId.username


# ✅ SERVICE STAFF MODEL
class ServiceStaff(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name