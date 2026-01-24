from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_posted','photo']
    search_fields = ['title', 'content']
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'title_tag', 'author', 'category')
        }),
        ('내용', {
            'fields': ('content',),
            'description': 'Content는 비워둘 수 있습니다.'
        }),
        ('미디어', {
            'fields': ('photo',)
        }),
        ('상호작용', {
            'fields': ('likes',)
        }),
    )

admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ('post', 'author')
    list_display = ('post', 'author', 'date_commented', 'content')
    list_filter = ('author__username', 'date_commented')
    search_fields = ('author__username', 'post__title')
    ordering = ('-date_commented',)