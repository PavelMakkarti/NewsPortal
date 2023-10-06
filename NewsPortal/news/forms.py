from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['title', 'postCategory', 'text', 'postAuthor', 'categoryType']

       def clean(self):
           cleaned_data = super().clean()
           description = cleaned_data.get("description")
           if description is not None and len(description) < 20:
               raise ValidationError({
                   'Заголовок не должен совпадать с категорией'
               })

           return cleaned_data