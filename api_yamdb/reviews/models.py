from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


ROLES_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]
MAX_LENGTH_SHORT = 50
MAX_LENGTH_MED = 150
MAX_LENGTH_LONG = 254


class User(AbstractUser):
    username = models.CharField(
        'Username', max_length=MAX_LENGTH_MED, unique=True
    )
    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH_LONG,
        help_text='Specify your email.',
        unique=True,
    )
    role = models.CharField(
        'Roles', choices=ROLES_CHOICES, default='user', max_length=14
    )
    bio = models.TextField(
        'Biography', blank=True, null=True, help_text='Short bio here.'
    )
    first_name = models.CharField(
        'First name', max_length=MAX_LENGTH_MED, null=True, blank=True
    )
    last_name = models.CharField(
        'Last name', max_length=MAX_LENGTH_MED, null=True, blank=True
    )
    access_code = models.CharField(
        max_length=8, default=None, blank=True, null=True
    )


class Category(models.Model):
    name = models.CharField('Category', max_length=MAX_LENGTH_SHORT)
    slug = models.SlugField('Slug', max_length=MAX_LENGTH_SHORT)


class Genre(models.Model):
    name = models.CharField('Category', max_length=MAX_LENGTH_SHORT)
    slug = models.SlugField('Slug', max_length=MAX_LENGTH_SHORT)


class Title(models.Model):
    name = models.CharField('Title', max_length=MAX_LENGTH_MED)
    year = models.IntegerField('Year of release')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles_category',
    )
    genre = models.ManyToManyField(Genre, blank=True)

    class Meta:
        ordering = ['year']

    def __str__(self):
        return self.name


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
        'Rating',
        help_text='Set rating to the choosen title.',
        validators=[MaxValueValidator(10), MinValueValidator(1)],
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
