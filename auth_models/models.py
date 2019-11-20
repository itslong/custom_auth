from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4


class CustomUserManager(BaseUserManager):
  def create_user(self, email, username=None, first_name=None, last_name=None, password=None):
    if not email:
      raise ValueError('You must enter a valid email.')

    user = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password, username=None, first_name=None, last_name=None):
    user = self.create_user(
      email = email,
      username = username,
      first_name = first_name,
      last_name = last_name,
      password = password
    )

    user.is_admin = True
    user.is_superuser = True
    user.save(using=self._db)
    return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
  """
  from AbstractBaseUser: last_login, password
  from PermissionsMixin: groups, user_permissions
  """
  email = models.EmailField(max_length=254, unique=True)
  username = models.CharField(max_length=128, blank=True, null=True, unique=True)
  first_name = models.CharField(max_length=50, blank=True, null=True)
  last_name = models.CharField(max_length=50, blank=True, null=True)
  password = models.CharField(max_length=128, verbose_name='password')
  
  created_at = models.DateTimeField(auto_now_add=True, editable=False)
  updated_at = models.DateTimeField(auto_now=True)
  last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')

  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)

  is_superuser = models.BooleanField(
    default=False,
    help_text='Designates that this user has all permissions without explicitly assigning them.',
    verbose_name='superuser status'
  )

  groups = models.ManyToManyField(
    blank=True,
    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    related_name='user_set',
    related_query_name='user',
    to='auth.Group',
    verbose_name='groups'
  )

  class Meta:
    unique_together = ('email', 'username', )

  user_permissions = models.ManyToManyField(
    blank=True,
    help_text='Specific permissions for this user.',
    related_name='user_set',
    related_query_name='user',
    to='auth.Permission',
    verbose_name='user permissions'
  )

  objects = CustomUserManager()
  USERNAME_FIELD = 'email'
  # REQUIRED_FIELDS = ['email']

  def __str__(self):
    return self.email

  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    return True

  def has_module_perms(self, app_label):
    "Does the user have permissions the app `app_label`?"
    return True

  @property
  def is_staff(self):
    "Is the user a member of staff?"
    return self.is_admin

  # creates a user hashed string in place of a username if the username field is left blank
  # def clean(self):
  #   if getattr(self, 'username', None) is None:
  #     self.username = 'user-' + str(uuid4())
