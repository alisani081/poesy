from django import forms
from .models import Poem, Topic

class PoemForm(forms.ModelForm):

    class Meta:
        model = Poem
        fields = ('topic', 'title', 'content')
        widgets = {
            'topic': forms.Select(attrs={ 
                'class': 'ui search dropdown'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Your Poem Title'
            }),
            'content': forms.Textarea(attrs={ 
                'placeholder': 'Compose your poem...'
            }),            
        }
