from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'sumary', 'video')
        labels = {
            'title': 'Título',
            'sumary': 'Resumen',
            'video': 'Video',
        }
        error_messages = {
            'title': {
                'max_length': "El nombre es demasiado largo",
            },
        }

class XMLForm(forms.Form):
   xml = forms.FileField()
   password = forms.CharField(max_length=64)
