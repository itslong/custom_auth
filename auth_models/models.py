from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
  def create_user(self, email, first_name=None, last_name=None, password=None):
    if not email:
      raise ValueError('You must enter a valid email.')

    user = self.model(
      email = self.normalize_email(email),
      first_name = first_name,
      last_name = last_name
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password, first_name=None, last_name=None):
    user = sefl.create_user(
      email = email,
      first_name = first_name,
      last_name = last_name,
      password = password
    )

    user.is_admin = True
    user.save(using=self._db)
    return user


class CustomUser(models.Model):
  email = models.EmailField(max_length=254, unique=True)
  first_name = models.CharField(max_length=50, blank=True)
  last_name = models.CharField(max_length=50, blank=True)
  
  created_at = models.DateTimeField(auto_now_add=True, editable=False)
  updated_at = models.DateTimeField(auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)


  objects = CustomUserManager()
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
    return self.email

  @property
  def is_staff(self):
    return self.is_admin
