from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='profile',
    )
    # post_set (FK)
    # comment_set (FK)
    # post_set (MMF) -> 충돌 => like_posts

    # self: user와 user를 연결
    followings = models.ManyToManyField( # 내가 follow
        'self',
        related_name='followers',
        symmetrical=False, # 대칭구조를 False로: 1 follow 2 != 2 follow 1
        )
    # user_set => followers # 나를 follow