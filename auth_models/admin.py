from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from auth_models.models import CustomUser


class UserCreationForm(forms.ModelForm):
  """
  Create new user form with a repeated password field and all required fields.
  """
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

  class Meta:
    model = CustomUser
    fields = ('email', 'first_name', 'last_name')

  def clean_pw2(self):
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Passwords don't match")
    return password2

  def save(self, commit=True):
    # save the provided password in hashed format
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password1'])
    if commit:
      user.save()
    return user


class UserChangeForm(forms.ModelForm):
  """
  Form to update users but replaces the password field with admin's password hash display field.
  """
  password = ReadOnlyPasswordHashField(
    label=('Password'),
    help_text=("Raw passwords are not stored, so there is no way to see "
               "this user's password, but you can change the password "
               "using <a href=\"../password/\">this form</a>.")
  )

  class Meta:
    model = CustomUser
    fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

  def clean_password(self):
    """
    Regardless of what the user provides, return the initial value.
    This is done here, rather than on the field, 
    because the field does not have access to the initial value.
    """
    return self.initial['password']


class CustomUserAdmin(BaseUserAdmin):
  """
  Override and register the default admin
  """

  # include forms to add and change user instances
  update_user_form = UserChangeForm
  create_user_form = UserCreationForm

  # provides fields to be used in displaying the Custom User model
  list_display = (
    'email', 'last_name', 'first_name', 'created_at', 
    'last_login', 'is_staff', 'is_admin', 'is_superuser'
  )
  list_filter = ('is_admin', 'last_name')
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name')}),
    ('Permissions', {'fields': ('is_admin', 'is_superuser', 'user_permissions')}),
  )

  # add_fieldsets is not a standard ModelAdmin attribute.
  # CustomUserAdmin overrides get_fieldsets to use this attribute when creating a user
  add_fieldsets = (
    (None, {
        'classes': ('wide', ),
        'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
      }
    ),
  )

  search_fields = ('email', 'last_name', )
  ordering = ('email', )
  filter_horizontal = ()

# register the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# unregister the Group model from admin since Django's built-in permissions are not used
# or add PermissionsMixin to the Custom User Model to use Django's built-in permissions
# admin.site.unregister(Group)

