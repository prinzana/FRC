from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyGraceAdmin, MyGraceUser

# Form for creating a MyGraceAdmin (admin user)
class MyGraceAdminCreationForm(UserCreationForm):
    class Meta:
        model = MyGraceAdmin
        fields = ('username', 'email', 'fullname')  # Only include fields needed for creation

# Form for changing a MyGraceAdmin
class MyGraceAdminChangeForm(UserChangeForm):
    class Meta:
        model = MyGraceAdmin
        fields = ('username', 'email', 'fullname', 'is_active', 'is_staff', 'is_superuser')  # Include necessary fields for changing

# Form for creating a MyGraceUser (regular user)
class MyGraceUserCreationForm(UserCreationForm):
    class Meta:
        model = MyGraceUser
        fields = ('username', 'email', 'fullname')  # Only include fields needed for creation

# Form for changing a MyGraceUser
class MyGraceUserChangeForm(UserChangeForm):
    class Meta:
        model = MyGraceUser
        fields = ('username', 'email', 'fullname', 'is_active')  # Include necessary fields for changing
