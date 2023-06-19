from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='', max_length=100, widget=forms.EmailInput(attrs={'placeholder':'Email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('There is no user registered with the specified email address!')
        return email

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'New Password'}))
    new_password2 = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Confirm New Password'}))

    def __init__(self, user, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''
