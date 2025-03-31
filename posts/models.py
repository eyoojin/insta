from django.db import models

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image')
    # 필수 옵션 'upload_to': 이미지가 저장되는 공간