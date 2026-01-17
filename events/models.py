from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile 
import os

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    web = models.URLField('Website Address', blank=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    venue_image = models.ImageField(null=True, blank=True, upload_to="venues/images/")
    
    def get_absolute_url(self):
        return reverse("venue-details", kwargs={"pk": self.pk})
    

    def __str__(self):
        return self.name

class Favorite(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='idol_images/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:

            img = Image.open(self.image)
            if img.height > 200 or img.width > 200:
                img.thumbnail((200, 200))
            thumb_io = BytesIO()
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(thumb_io, format='JPEG')
            filename = os.path.basename(self.image.name)
            self.thumbnail.save(f'thumbnail_{filename}', ContentFile(thumb_io.getvalue()), save=False)
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField('Event Name', max_length=120)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField('시작일시', blank=True, null=True)
    end_date = models.DateTimeField('종료일시', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    attendees = models.ManyToManyField(Favorite, blank=True)

    def __str__(self):
        return self.title
