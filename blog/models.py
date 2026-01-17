from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('blog:index')
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.SlugField(max_length=120, blank=True, null=True, allow_unicode=True)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    
    def __str__(self):
        return f'{self.title} - {self.author.username}'
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.title_tag:
            self.title_tag = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['updated_at','-date_posted']

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.content[:10]}'
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.post.pk})
    
    class Meta:
        ordering = ['-date_commented']