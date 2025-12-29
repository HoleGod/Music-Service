from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Song, Playlist, Comment

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=30, label="Full name...")
	last_name = forms.CharField(max_length=30, label="Pseudo...")
	#first name -> pseudo
	class Meta:
		model = User
		fields = ["username", "first_name","last_name", "email", "password1", "password2"]

class AddComment(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["label", "text"]
		widgets = {
			"label": forms.TextInput(attrs={
				"class": "form-control bg-dark text-white",
				"placeholder": "Title...",
			}),
			"text": forms.Textarea(attrs={
				"class": "form-control bg-dark text-white",
				"rows": 6,
				"placeholder": "Write comment...",
			}),
		}

class AddSong(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["author", "title", "text", "audio", "cover_image", "genre", "release_year", "key", "bpm",]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control bg-dark text-white",
                "placeholder": "Title..."
            }),
            "author": forms.TextInput(attrs={
                "class": "form-control bg-dark text-white",
                "placeholder": "Title..."
            }),
            "text": forms.Textarea(attrs={
                "class": "form-control bg-dark text-white",
                "rows": 6,
                "placeholder": "Write desc..."
            }),
            "audio": forms.ClearableFileInput(attrs={
                "class": "form-control bg-dark text-white",
                "accept": "audio/*"
            }),
            "cover_image": forms.ClearableFileInput(attrs={
                "class": "form-control bg-dark text-white",
                "accept": "image/*"
            }),
            "genre": forms.Select(attrs={
				"class": "form-select bg-dark text-white"
			}),
			"release_year": forms.DateInput(attrs={
				"class": "form-control bg-dark text-white",
				"placeholder": "Year..."
				},
            ),
			"key": forms.Select(attrs={
				"class": "form-select bg-dark text-white"
			}),
			"bpm": forms.NumberInput(attrs={
				"class": "form-control bg-dark text-white",
				"placeholder": "BPM..."
			}),
        }

class AddPlayList(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["title","is_public"]
        
        widgets = {
			'title': forms.TextInput(attrs={
				'class': 'form-control bg-dark text-white',
				"placeholder": "Title..."
			}),
			"is_public": forms.Select(choices=[
					(True, "Public"),
					(False, "Private")
				], attrs={
					"class": "form-select bg-dark text-white"
				}),
		}