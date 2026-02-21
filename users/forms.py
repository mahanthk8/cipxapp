from pyexpat.errors import messages

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from regions.models import Region

# User Registration Form

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)
    region = forms.ModelChoiceField(queryset=Region.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'region', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'USER'
        if commit:
            user.save()
        return user

# User Update Form (For Profile Updates)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'phone']


# Officer Creation Form (Admin Only)

class OfficerCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'region', 'star', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'OFFICER'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
# Officer Update Form (Admin Only)
class OfficerUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'region', 'star']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'OFFICER'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Admin Registration Form (Admin Only)
class AdminRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'ADMIN'
        if commit:
            user.save()
        return user


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
