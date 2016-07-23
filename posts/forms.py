from django import forms
from .models import Post
import os

class PostForm(forms.ModelForm):
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
    content=forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2}))
