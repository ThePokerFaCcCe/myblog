from django.core.exceptions import ValidationError
from django_filters.rest_framework import FilterSet
from django.forms import Form

from .models import Category, Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['iexact', 'icontains'],
            'content': ['icontains'],
            'category_id': ['exact', 'in'],
            'author_id': ['exact', 'in']
        }


class RUDForm(Form):
    def clean(self):
        cleaned_data = super().clean()

        id = cleaned_data.get('id')
        slug = cleaned_data.get('slug')

        if id and slug:
            raise ValidationError("You have to enter either id or slug, not both!")
        elif not id and not slug:
            raise ValidationError("You have to enter id or slug!")

        return cleaned_data


class RUDFilter(FilterSet):
    class Meta:
        model = Post
        form = RUDForm
        fields = {
            'id': ['exact'],
            'slug': ['exact']
        }
