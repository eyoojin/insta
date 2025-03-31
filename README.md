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
- setting
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
media/
```

## 6. requirements.txt 추가
```shell
pip freeze >> requirements.txt
```

# Posts
## 7. Post - Read
- 경로 설정 `insta/urls.py` -> `posts/urls.py`
- 함수 생성 `posts/views.py`
- 페이지 생성
```html
<!-- posts/templates/index.html -->
{% for post in posts %}
    <p>{{post.content}}</p>
    <p>{{post.image}}</p>
    <p>{{post.image.url}}</p>
{% endfor %}
```

## 8. Post - Read 기능 업데이트
- 이미지 확인
```html
<!-- posts/templates/index.html -->
<img src="{{post.image.url}}" alt="">
```
- bootstrap 편하게 사용하기
    - `posts/templates/_card.html`에 card css 복사
```html
<!-- posts/templates/index.html -->
{% for post in posts %}
    {% include '_card.html' %}
{% endfor %}
```
```html
<!-- posts/templates/_card.html -->
<!-- 이 안은 for문 안쪽임 -->
<div class="card my-3" style="width: 18rem;">
    <div class="card-header">
        <p>username</p>
    </div>
    <img src="{{post.image.url}}" class="" alt="...">
    <div class="card-body">
        <p class="card-text">{{post.content}}</p>
        <p class="card-text">{{post.created_at}}</p>
    </div>
</div>
```

## 9. navbar
- navbar
    - `../templates/_nav.html` 생성

## 10. Post - Create
- 버튼 생성 `../templates/_nav.html`
- 경로 설정 `posts/urls.py`
- Form
```python
# posts/forms.py
from django.forms import ModelForm
```
- 함수 생성(GET 요청) `posts/views.py`
- 페이지 생성
```html
<!-- posts/templates/create.html -->
<!-- 사진을 가져오려면 인코딩타입 변경 -->
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
```
- 함수 생성(POST 요청)
```python
# posts/views.py
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
```
- bootstrap 적용
```shell
pip install django-bootstrap5
```
```python
# insta/settings.py
INSTALLED_APPS = ['django_bootstrap5']
```
```html
<!-- posts/templates/create.html -->
{% load django_bootstrap5 %}

{% bootstrap_form form %}
<input type="submit" class="btn btn-primary">
```

## 11. image resize 기능 추가
```shell
pip install django-resized
```
```python
# posts/models.py
from django_resized import ResizedImageField

# image = models.ImageField(upload_to='image')

image = ResizedImageField(
    size=[500, 500],
    crop=['middle', 'center'],
    upload_to='image/%Y/%m', # 년도와 월을 기준으로 폴더를 만듦
)
```
- 사진 폴더/ DB 초기화
- requirements update
```shell
pip freeze > requirements.txt
```
- `>>`: 현재 파일에 추가
- `>`: 현재 파일에 덮어쓰기

# Acoounts
## 12. startapp
- 앱 등록

## 13. User modeling/ migration
```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='profile',
    )
```
```python
# insta/settings.py
AUTH_USER_MODEL = 'accounts.User'
```
```python
# posts/models.py
from django.conf import settings

# User와 Post 1:N 연결
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```
- migration
    - error
        - 1. default 값 설정
        - 2. model 수정 or DB 날리기
- 다시 migration

## 14. Signup - Create
- 경로 설정 `insta/urls.py` -> `accounts/urls.py`
- form
```python
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'profile_image', )
```
- 함수 생성(GET 요청) `accounts/views.py`
- 페이지 생성 `accounts/templates/signup.html`
    - `create.html`과 동일
- 함수 생성(POST 요청) `accounts/views.py`

## 15. Login - Create 
- 경로 설정 `accounts/urls.py`
- form
```python
# accounts/forms.py
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    pass
```
- 함수 생성(GET 요청) `accounts/views.py`
- 페이지 생성 `accounts/templates/login.html`
    - `enctype` 빼고 `signup.html`과 동일
- 함수 생성(POST 요청)
```python
# accounts/views.py
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():

            # user 정보 가져오기
            user = form.get_user()

            # login 처리 -> session 만들기
            auth_login(request, user)

            return redirect('posts:index')
```


---
### commit message 수정
```shell
git commit --amend
```
- i: insert mode 설정 -> 수정
- esc: inset mode 해제
- :wq
