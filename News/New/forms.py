from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields =['title', 'postCategory', 'text', 'postAuthor', 'categoryType']

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        postCategory = cleaned_data.get('postCategory')
        title = cleaned_data.get('title')

        if title == postCategory:
            raise ValidationError(
                'Заголовок не должен совпадать с категорией'
            )
        return  cleaned_data


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user


