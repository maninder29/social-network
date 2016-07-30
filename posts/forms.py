from django import forms
from .models import Post,UserProfile
import os

class PostForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={'class':'mdl-textfield__input','rows':4}))
    # media=forms.FileField(widget=forms.FileInput(attrs={'class':"mdl-button mdl-js-button mdl-button--raised mdl-button--colored"}))
    class Meta:
        model = Post
        fields = [
            "content",
            "media"
        ]
    def clean_media(self):
        media=self.cleaned_data.get("media")
        if media:
            name, extension = os.path.splitext(media.name)
            if extension in [".3gp",".3GP",".avi",".AVI",".mkv",".MKV"]:
                raise forms.ValidationError("Only mp4 and WebM video formats are supported :(")
            return media

class CommentForm(forms.Form):
    content=forms.CharField(label='', widget=forms.Textarea(attrs={'class':'mdl-textfield__input','rows':2}))



class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['profile_pic','gender','phone','dob','address','relationship_status']
        widgets={
            'profile_pic':forms.FileInput(attrs={'class':"mdl-button mdl-js-button mdl-button--raised mdl-button--colored"}),
            'gender':forms.TextInput(attrs={'class':'mdl-textfield__input'}),
            'phone':forms.TextInput(attrs={'class':'mdl-textfield__input'}),
            'dob':forms.TextInput(attrs={'class':'mdl-textfield__input'}),
            'address':forms.TextInput(attrs={'class':'mdl-textfield__input', 'rows':4}),
            'relationship_status':forms.TextInput(attrs={'class':'mdl-textfield__input'}),
        }
