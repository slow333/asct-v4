from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, null=True, blank=True)
    birth_day = models.DateField(null=True, blank=True)
    ROLES = (
        ('op', '운영자'),
        ('mg', '관리자'),
        ('tmp', '임시 사용자'),
    )
    role = models.CharField(max_length=6, choices=ROLES, default='op', blank=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f"{self.user.username} Profile"
