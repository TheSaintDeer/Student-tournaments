from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main.models import Player, Post


# Create your forms here.
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].label = 'First name:'
        self.fields['last_name'].label = 'Last name:'
        self.fields['username'].label = 'Username:'
        self.fields['email'].label = 'Email:'


    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']



class UpdatePlayerForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())
    bio = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Say something...',
            'rows': 5,
        }))

    def __init__(self, *args, **kwargs):
        super(UpdatePlayerForm, self).__init__(*args, **kwargs)

        self.fields['avatar'].label = 'Change avatar:'
        self.fields['avatar'].required = False

        self.fields['bio'].label = 'Bio:'
        self.fields['bio'].required = False


    class Meta:
        model = Player
        fields = ['avatar', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = ['author', 'updated', 'created', ]
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'required': True, 
                'placeholder': 'Say something...'
            }),
        }