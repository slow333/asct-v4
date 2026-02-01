from django.contrib import admin
from django.utils.html import format_html
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'image_preview', 'role','phone']
    search_fields = ['user__username',]
    list_filter = ('role',)
    list_editable =('role',)
    list_per_page = 20
    list_select_related = ['user']
    ordering = ('user__username',)

    def image_preview(self, profile):
        if profile.image:
            return format_html('<img src="{}" style="width: 30px; height: auto;" />', profile.image.url)
        return "No Image"
    image_preview.short_description = 'Profile Image'

# 기본 User 모델의 등록을 취소합니다.
admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

@admin.register(User)
class UserCustomAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ['username', 'first_name', 'get_profile_image', 'is_staff', 'is_active']
    list_editable = ['is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_per_page = 20
    ordering = ('username',)
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

    def get_profile_image(self, instance):
        if hasattr(instance, 'profile') and instance.profile.image:
            return format_html('<img src="{}" style="width: 30px; height: auto;" />', instance.profile.image.url)
        return "No Image"
    get_profile_image.short_description = 'Profile Image'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserCustomAdmin, self).get_inline_instances(request, obj)