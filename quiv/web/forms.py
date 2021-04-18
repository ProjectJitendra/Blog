from django import forms
from web.models import  Comment, ContactUs
from user.models import User

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
