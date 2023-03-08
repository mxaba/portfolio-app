from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email Address'}
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'})
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name'}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            try:
                self.instance.profile
            except Profile.DoesNotExist:
                Profile.objects.create(user=user)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        labels = {'profile_pic': 'Profile Picture'}
        exclude = ['user']
