from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from . import models
from ReviewsElicitation.settings import EMAIL_HOST_USER
import random

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    contact_number = forms.CharField(min_length=10, max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['email'].label = ''
        self.fields['contact_number'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def send_otp_email(self, request):
        email = self.cleaned_data['email']
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp

        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        print(otp)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("This email id is already registered.")
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        try:
            user_profile = models.UserProfile.objects.get(contact_number=contact_number)
        except models.UserProfile.DoesNotExist:
            return contact_number
        raise forms.ValidationError("This contact number is already registered.")
    

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['password'].label = ''

        self.fields['email'].help_text = ''
        self.fields['password'].help_text = ''

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("This email id is not registered.")
        if not user.check_password(password):
            raise forms.ValidationError("The password entered is either incorrect or invalid.")
        return self.cleaned_data


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(min_length=6, max_length=6, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp'].label = ''


class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, widget=forms.FileInput)
    # remove_photo = forms.BooleanField(required=False)

    class Meta:
        model = models.UserProfile
        fields = ['profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.profile_image:
            self.fields['remove_photo'] = forms.BooleanField(required=False)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('remove_photo'):
            instance.profile_image.delete()
            instance.profile_image = None

        if commit:
            instance.save()

        return instance



class ProfileDetailsForm(forms.Form):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Not specified'),
    )

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    contact_number = forms.CharField(min_length=10, max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.user = user

        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['contact_number'].label = 'Contact Number'
        self.fields['gender'].label = 'Gender'

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

            profile = models.UserProfile.objects.get(user=user)
            self.fields['contact_number'].initial = profile.contact_number
            self.fields['gender'].initial = profile.gender

    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if len(contact_number) != 10:
            raise forms.ValidationError("Contact number should be a 10-digit number.")
        
        user = self.user

        if models.UserProfile.objects.exclude(user=user).filter(contact_number=contact_number).exists():
            raise forms.ValidationError("This contact number is already taken.")
        return contact_number
    
    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = models.UserProfile.objects.get(user=user)

        profile.contact_number = self.cleaned_data['contact_number']
        profile.gender = self.cleaned_data['gender']
        profile.save()


class BioForm(forms.Form):
    bio = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Write something about yourself...'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['bio'].label = ''
        self.fields['bio'].initial = user.userprofile.bio

    def save(self, user):
        profile = models.UserProfile.objects.get(user=user)
        profile.bio = self.cleaned_data['bio']
        profile.save()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['review', 'review_rating', 'is_anonymous']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review'].label = ''
        self.fields['is_anonymous'].label = 'Anonymous Review'
        self.fields['review_rating'].label = ''

        self.fields['review'].widget.attrs['placeholder'] = 'Write your review here...'
        self.fields['review_rating'].widget = forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '10', 'step': '1'})
        self.fields['review_rating'].widget.attrs['id'] = 'review-rating'


    def clean(self):
        cleaned_data = super().clean()
        to_username = self.instance.to_user
        from_username = self.instance.from_user

        existing_review = models.Review.objects.filter(to_user=to_username, from_user=from_username).exclude(id=self.instance.id)

        if existing_review:
            raise forms.ValidationError('You have already reviewed this user!')
        
        return cleaned_data

        
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''

        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''
