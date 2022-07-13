from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES_CHOICES = [
    ('USER', 'USER'),
    ('MODERATOR', 'MODERATOR'),
    ('ADMIN', 'ADMIN'),
]


class User(AbstractUser):
    username = models.CharField('Username', max_length=50, unique=True)
    email = models.EmailField(
        'Email', max_length=100, help_text='Specify your email.', unique=True
    )
    role = models.CharField(
        'Roles', choices=ROLES_CHOICES, default='USER', max_length=14
    )
    bio = models.TextField(
        'Biography', blank=True, null=True, help_text='Short bio here.'
    )
    first_name = models.CharField('First name', max_length=50)
    last_name = models.CharField('Last name', max_length=50)
    access_code = models.CharField(
        max_length=8, default=None, blank=True, null=True
    )


class Category(models.Model):
    name = models.CharField('Category', max_length=50)
    slug = models.SlugField('Slug', max_length=50)


class Genre(models.Model):
    name = models.CharField('Category', max_length=50)
    slug = models.SlugField('Slug', max_length=50)


class Title(models.Model):
    name = models.CharField('Title', max_length=100)
    year = models.IntegerField('Year of release')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles_category',
    )
    genre = models.ManyToManyField(Genre, blank=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
    )
    text = models.TextField('Review', help_text='Write your review here.')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_authors'
    )
    score = models.IntegerField(
        'Rating', help_text='Set rating to the choosen title.'
    )
    pub_date = models.DateTimeField('Date of publishing', auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField('Comment', help_text='Write your comment here.')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments_authors'
    )
    pub_date = models.DateTimeField('Date of publishing', auto_now_add=True)
