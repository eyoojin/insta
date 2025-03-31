# insta

- 프로젝트 이름: 서비스 이름
- 모델 이름: 앱 이름

# Setting
## 0. .gitignore
- 가상환경 생성/ 활성화
- django 설치
- .gitignore

## 1. startproject/ startapp
- 앱 등록

## 2. base.html 기본 구조
- templates 등록

## 3. Post modeling/ migration
- modeling
    - ImageField
```python
# posts/models.py
image = models.ImageField(upload_to='image')
# 필수 옵션 'upload_to': 이미지가 저장되는 공간
```
- makemigrations
    - error
```shell
pip install pillow
```
- migrate

## 4. admin에 Post 모델 등록
```python
# posts/admin.py
from .models import Post

admin.site.register(Post)
```

## 5. .gitignore에 image 폴더 추가
- createsuperuser 생성
- admin 페이지 확인
- image 폴더 .gitignore 설정
```git
image/
```

## 6. requirements.txt 추가
```shell
pip freeze >> requirements.txt
```

# Posts
## 7. Post - Read
- 경로 설정
- 함수 생성
- 페이지 생성
```html
<!-- posts/templates/index.html -->
{% for post in posts %}
    <p>{{post.content}}</p>
    <p>{{post.image}}</p>
{% endfor %}
```

## 8. media 설정
```python
# settings.py
MEDIA_ROOT = BASE_DIR / 'media'
# 업로드한 사진을 저장한 위치(실제 폴더 경로)

MEDIA_URL = '/media/'
# 미디어 경로를 처리할 URL
```
```python
# insta/urls.py
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + concatenation
# (사용자에게 보여주는 경로, 실제로 가야할 경로)
```
- 사용자에게 이미지 보여줄 준비 완료

## 9. Read 기능 업데이트
- 이미지 확인
```html
<!-- posts/index.html -->
<img src="{{post.image.url}}" alt="">
```
- `templates/_card.html`에 card css 복사
```html
<!-- posts/index.html -->
{% for post in posts %}
        {% include '_card.html' %}
{% endfor %}
```
```html
<!-- posts/_card.html -->
<div class="card my-3" style="width: 18rem;">
    <div class="card-header">
        <p>username</p>
    </div>
    <img src="{{post.image.url}}" class="" alt="...">
    <div class="card-body">
      <!-- <h5 class="card-title">Card title</h5> -->
      <p class="card-text">{{post.content}}</p>
      <p class="card-text">{{post.created_at}}</p>
      <!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
    </div>
</div>
```
