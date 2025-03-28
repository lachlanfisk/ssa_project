from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    nickname = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nickname']

    def save(self, commit=True):
        user = super().save(commit=False)       
        if commit:
            user.save()
            profile = user.profile
            profile.nickname = self.cleaned_data['nickname']
            profile.save()
<<<<<<< HEAD
        return user
=======
        return user

class TopUpForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=5,
        decimal_places=2,
        label="Amount to Top-Up",
        error_messages={
            'min_value': "Please enter an amount greater than $0.00.",
            'invalid': "Enter a valid amount in dollars and cents.",
        }
    )
>>>>>>> d1899b9 (initial commit)
