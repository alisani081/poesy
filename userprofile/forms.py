from django.contrib.auth.models import User
from userprofile.models import Profile
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'required': 'required',
                'placeholder': 'Your First name',
                'maxlength': 30
            }),
            'last_name': forms.TextInput(attrs={
                'required': 'required',
                'placeholder': 'Your Last name',
                'maxlength': 30
            }),            
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'bio')
        widgets = {
            'location': forms.TextInput(attrs={
                'placeholder': 'Your City, State or Country'
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell us about yourself?',
                'maxlength': 160,
                'rows': 8,
                'data-length': 160,
                'class': 'char-textarea'
            }),
        }

class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)