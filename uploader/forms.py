from django import forms
from .models import Original, Temp


class PostForm(forms.ModelForm):
    class Meta:
        model = Original
        fields = ['image', 'image_url']
        image_url = forms.ImageField()


class TestForm(forms.Form):
    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)
    class Meta:
        model = Temp
        fields = ['width', 'height']

