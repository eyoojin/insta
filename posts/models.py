from django.db import models
from django_resized import ResizedImageField

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='image')
    # 필수 옵션 'upload_to': 이미지가 저장되는 공간

    image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='image/%Y/%m', # 년도와 월을 기준으로 폴더를 만듦
    )