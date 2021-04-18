from ckeditor.fields import RichTextField
from django.db.models import Count
from django.utils.datetime_safe import datetime
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.utils.text import slugify
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=255, unique=True)
    content = RichTextField()
    img = models.ImageField(upload_to='gallery', )
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField( null=True, blank=True)
    likes = models.ManyToManyField('user.User', related_name='likes', blank=True)
    tag = models.ManyToManyField('Tag', related_name='tag')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def total_like(self):
        return self.likes.count()

    def get_date(self):
        time = datetime.now()
        if self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + " days ago"
        else:
            if self.created_at.year == time.year:
                return str(time.month - self.created_at.month) + " months ago"
        return self.created_at

    @property
    def related_posts(self):
        return Post.objects.filter(category=self.category).exclude(id=self.id)[:5]

    @property
    def get_popular_posts(self):
        return Post.objects.annotate(likes_count=Count('likes')).filter(likes_count__gt=2).order_by('-created_at')[:5]



class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    user = models.CharField(max_length=255,)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment


class ContactUs(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.email