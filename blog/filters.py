from django_filters.rest_framework import FilterSet

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


class PostDetailFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'id': ['exact'],
            'slug': ['exact']
        }


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'id': ['exact'],
            'slug': ['exact']
        }
