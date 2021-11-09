from django_filters.rest_framework import FilterSet

from .models import Category, Post


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'id': ['exact'],
            'slug': ['exact']
        }
