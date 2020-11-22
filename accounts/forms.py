from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    terms = forms.BooleanField(required=True, error_messages={
                               'required': 'You must accept our privacy policy and terms.'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'terms')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')
