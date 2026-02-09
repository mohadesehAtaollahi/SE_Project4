from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserSecurity


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        min_length=8,
        help_text="Password must be at least 8 characters long"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    security_question = forms.ChoiceField(
        choices=UserSecurity.SECURITY_QUESTIONS,
        label="Security Question",
        help_text="Select a question for password recovery"
    )

    security_answer = forms.CharField(
        max_length=255,
        label="Your Answer",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your answer here',
            'autocomplete': 'off'
        }),
        help_text="Remember this answer for password recovery"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        labels = {
            "username": "Username",
            "email": "Email",
            "password": "Password"
        }
        help_texts = {
            "username": "Your username for login"
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")


        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already registered")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # هش کردن رمز

        if commit:
            user.save()
            UserSecurity.objects.create(
                user=user,
                question=self.cleaned_data['security_question'],
                answer=self.cleaned_data['security_answer']
            )

        return user



class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )

