# Create your models here.
from django.db import models

class ImageData(models.Model):
    image_url = models.URLField(unique=True)  
    md5_hash = models.CharField(max_length=32) 
    phash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)  

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f"ImageData: {self.image_url}"