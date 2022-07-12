from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES_CHOICES = [
    ('USER', 'USER'),
    ('MODERATOR', 'MODERATOR'),
    ('ADMINISTRATOR', 'ADMINISTRATOR'),
]


class Users(AbstractUser):
    username = models.CharField('Username', max_length=50)
    email = models.EmailField('Email', help_text='Specify your email.')
    role = models.CharField(
        'Roles', choices=ROLES_CHOICES, default='USER', max_length=14
    )
    bio = models.TextField(
        'Biography', blank=True, null=True, help_text='Short bio here.'
    )
    first_name = models.CharField('First name', max_length=50)
    last_name = models.CharField('Last name', max_length=50)


class Category(models.Model):
    name = models.CharField('Category', max_length=50)
    slug = models.CharField('Slug', max_length=50)


class Genre(Category):
    ...


class Titles(models.Model):
    name = models.CharField('Title', max_length=100)
    year = models.IntegerField('Year of release')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(Genre, blank=True, null=True)


class Review(models.Model):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
    )
    text = models.TextField('Review', help_text='Write your review here.')
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        'Rating', help_text='Set rating to the choosen title.'
    )
    pub_date = models.DateTimeField('Date of publishing', auto_now_add=True)


class Comments(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField('Comment', help_text='Write your comment here.')
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Date of publishing', auto_now_add=True)
