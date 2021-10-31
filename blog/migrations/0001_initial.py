# Generated by Django 3.2.8 on 2021-10-31 12:23

import blog.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import picturic.fields
import picturic.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(2, 'first name must have 2 characters or more')], verbose_name='first name')),
                ('last_name', models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(2, 'last name must have 2 characters or more')], verbose_name='last name')),
                ('bio', models.TextField(blank=True, max_length=160, null=True, verbose_name='Biography')),
                ('profile_image', picturic.fields.PictureField(blank=True, max_length=9999, upload_to=picturic.utils.upload_to_path, verbose_name='Profile image')),
                ('email', models.EmailField(error_messages={'unique': 'An account with that email already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text="Staff's rank is lower than superuser", verbose_name='staff status')),
                ('is_author', models.BooleanField(default=False, help_text='Authors can write post and create category', verbose_name='author status')),
                ('is_vip', models.BooleanField(default=False, verbose_name='VIP status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. ', verbose_name='active status')),
                ('rank_expire_date', models.DateTimeField(blank=True, help_text="The date who user's rank will be expired", null=True, verbose_name='Rank expire date')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', blog.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, auto_created=True, editable=False)),
                ('title', models.CharField(max_length=40, verbose_name='title')),
                ('description', models.TextField(max_length=120, verbose_name='description')),
                ('picture', picturic.fields.PictureField(blank=True, max_length=9999, null=True, upload_to=picturic.utils.upload_to_path, verbose_name='Picture')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='title')),
                ('content', models.TextField(verbose_name='Content')),
                ('picture', picturic.fields.PictureField(blank=True, max_length=9999, null=True, upload_to=picturic.utils.upload_to_path, verbose_name='Picture')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.category', verbose_name='Category')),
            ],
        ),
    ]
