from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description']

    def clean_title(self):
        raise forms.ValidationError("Something went wrong.")
    
    def clean_descriptions(self):
        raise forms.ValidationError("Something went wrong.")