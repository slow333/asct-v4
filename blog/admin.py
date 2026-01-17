from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_posted']
    search_fields = ['title', 'content']

admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ('post', 'author')
    list_display = ('post', 'author', 'date_commented', 'content')
    list_filter = ('author__username', 'date_commented')
    search_fields = ('author__username', 'post__title')
    ordering = ('-date_commented',)