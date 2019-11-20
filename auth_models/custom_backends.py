from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
  """
  https://stackoverflow.com/questions/37332190/django-login-with-email/54889351#54889351
  Allows username or email to be used for authentication.
  username and email must be set to unique
  """
  def authenticate(self, request, username=None, password=None, **kwargs):
    try:
      user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
    except UserModel.DoesNotExist:
      UserModel().set_password(password)
    else:
      if user.check_password(password) and self.user_can_authenticate(user):
        return user

  def get_user(self, user_id):
    try:
      user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
      return None

    return user if self.user_can_authenticate(user) else None
   