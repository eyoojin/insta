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

            # login 처리 -> session 발급
            auth_login(request, user)

            return redirect('posts:index')
```

## 16. Logout - Delete
- 경로 설정 `accounts/urls.py`
- 함수 생성 
```python
# accounts/views.py
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('posts:index')
```
- 버튼 생성 + navbar 수정(if)
```html
<!-- ../templates/_nav.html -->
{% if user.is_authenticated %}
```

# Posts
## 17. Post - Create/ Read Update
- PostForm `posts/forms.py`
- 함수
```python
# posts/views.py
post = form.save(commit=False)
post.user = request.user
post.save()
```
- login_required
```python
# posts/views.py
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
```
- html 수정
```html
<!-- posts/templates/_card.html -->
<img class="rounded-circle" src="{{post.user.profile_image.url}}" alt="">
<a href="">{{post.user.username}}</a>
```

## 18. 시간 설정/ icon 설정
- 시간 설정
    - django가 가진 함수 사용
```html
<!-- posts/templates/_card.html -->
<p class="card-text">{{post.created_at|timesince}} ago</p>
```
- icon 설정
    - `../templates/base.html`에 CDN 추가
```html
<!-- _nav.html -->
<a class="navbar-brand" href="{% url 'posts:index' %}">
    <i class="bi bi-instagram"></i>
    Insta⭐
</a>
```

## 19. Grid 시스템 적용
```html
<!-- posts/templates/index.html -->
<div class="row">
    {% for post in posts %}
        {% include '_card.html' %}
    {% endfor %}
</div>
```
```html
<!-- posts/templates/_card.html -->
<div class="card my-3 p-0 col-12 col-md-6 col-xl-4">
<div class="card my-3 p-0 col-12 offset-md-3 col-md-6">
```
- col-12: 전체를 12칸으로 나눔
    - md 사이즈가 되면 6칸/6칸
    - xl 사이즈가 되면 4칸/4칸/4칸

# Comment
## 20. Comment modeling/migration

## 21. Comment Create
- 경로 설정 `posts/urls.py`
- Form `posts/forms.py`
- 함수 생성 `posts/views.py`
    - index 화면에서 출력
- 페이지 생성 `posts/templates/_card.html`
```html
{% load django_bootstrap5 %}

<div class="card-footer">
    <form action="" method="POST">
        {% csrf_token %}
        {% bootstrap_form form %}
        <input type="submit">
    </form>
</div>
```
- 디자인
```html
<div class="row">
    <div class="col-9">
        {% bootstrap_form form show_label=False wrapper_class='' %}
        <!-- wrapper_class='mb-3'이 기본이라 없애줌 -->
    </div>
    <div class="col-2">
        <input type="submit" class="btn btn-primary">
    </div>
</div>
```
- form action
- 함수 생성 `posts/views.py`
```python
@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
        return redirect('posts:index')
```
- 로그인 했을 때만 댓글작성창이 보이도록 수정

## 22. Comment Read
- 페이지 수정 `posts/templates/_card.html`
```html
<div class="mt-2">
    {% for comment in post.comment_set.all %}
        <li>{{comment.user}} : {{comment.content}}</li>
    {% endfor %}
</div>
```

# M:N
- `User` -< `Like` >- `Post`
- User:Like = 1:N
- Post:LIke = 1:N

## 23. like 기능 modeling/migration
```python
# posts/models.py
class Post(models.Model):
    # 게시글 작성자(User와 Post 1:N 연결)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user와 연결되면서 post_set 생성
    
    # 게시글에 좋아요 누른 사람(User와 Post M:N 연결)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts', # 역참조에 사용하는 name 변경
    )
```
```python
# accounts/models.py
class User(AbstractUser):
    # post_set (FK)
    # post_set (MMF) -> 충돌 => like_posts
```

## 24. like 기능 구현
- 좋아요 버튼 달기
```html
<!-- posts/templates/_card -->
<a href="{% url 'posts:like' post.id %}">
      <i class="bi bi-heart"></i>
</a>
```
- 경로 설정 `posts/urls.py`
- 함수 생성
```python
# posts/views.py
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # 게시물 관점
    if post in user.like_posts.all():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)

    # 유저 관점
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)

    # 좋아요 버튼을 눌렀을 때
    # if 이미 좋아요한 상태라면
    #   좋아요 삭제
    # else 좋아요하지 않은 상태라면
    #   좋아요 추가

    return redirect('posts:index')
```
- 좋아요 if
```html
<!-- posts/templates/_card.html -->
<a href="{% url 'posts:like' post.id %}" class="text-reset text-decoration-none">
    {% if user in post.like_users.all %}
    <i class="bi bi-heart-fill" style="color: red;"></i>
    {% else %}
    <i class="bi bi-heart"></i>
    {% endif %}
</a>
```
- form에서 like_users 삭제
```python
# posts/forms.py
fields = ('content', 'image', )
exclude = ('user', 'like_users', )
```

## 25. profile 기능 구현
- 버튼 생성 `posts/templates/_card.html`
- 경로 설정 `accounts/urls.py`
- 함수 생성 `accounts/views.py`
```python
from .models import User

def profile(request, username):
    user_profile = User.objects.get(username=username)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)
```
- 페이지 생성 `accounts/templates/profile.html`
    - 레이아웃 잡기: 페이지를 사각형으로 나눠보기
```html
{% extends 'base.html' %}

{% block body %}
    <div class="row my-3">
        <div class="col-3">
            <img src="{{user_profile.profile_image.url}}" class="img-fluid rounded-circle" alt="">
        </div>
        <div class="col-9">
            <div class="row">
                <div class="col-3">{{user_profile.username}}</div>
                <div class="col-9">
                    <a href="{% url 'accounts:follow' user_profile.username %}" class="btn btn-primary">follow</a>
                </div>
            </div>
            <div class="container text-center">
                <div class="row">
                    <div class="col-4">
                        posts
                    </div>
                    <div class="col-4">
                        followers
                    </div>
                    <div class="col-4">
                        following
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        {% for post in user_profile.post_set.all %}
            <div class="col-4 p-0">
                <img src="{{post.image.url}}" class="img-fluid" alt="">    
            </div>
        {% endfor%}
    </div>
{% endblock %}
```
## 26. follow 기능을 위한 modeling/migration
- 모델
```python
# accounts/models.py
# self: user와 user를 연결
followings = models.ManyToManyField( # 내가 follow
    'self',
    related_name='followers',
    symmetrical=False, # 대칭구조를 False로: 1 follow 2 != 2 follow 1
    )
# user_set => followers # 나를 follow
```

## 27. follow 기능 추가
- 버튼 생성 `accounts/templates/profile.html`
- 경로 설정 `accounts/urls.py`
- 함수 생성 `accounts/views.py`
```python
def follow(request, username):
    me = request.user
    you = User.objects.get(username=username)

    # 내가 너의 팔로우목록에 있을 때
    if me in you.followers.all(): # 팔로우함
        you.followers.remove(me)
    else: # 팔로우 안함
        you.followers.add(me)  

    # 네가 나의 팔로우목록에 있을 때
    if you in me.followings.all():
        me.followings.remove(you)
    else:
        me.followings.add(you)

    return redirect('accounts:profile', username)
```
- 페이지 수정
```html
<!-- accounts/templates/profile.html -->
posts {{user_profile.post_set.all|length}}
```
- 오류 수정
```html
<!-- accounts/templates/profile.html -->
{% if user != user_profile %}
<div class="col-9">
    <a href="{% url 'accounts:follow' user_profile.username %}" class="btn btn-primary">follow</a>
</div>
{% endif %}
```
```python
if me == you:
    return redirect('accounts:profile', username)
```
- login_required

## 28. follow if
```html
<!-- accounts/templates/profile.html -->
<div class="col-9">
    {% if user in user_profile.followers.all %}
        <a href="{% url 'accounts:follow' user_profile.username %}" class="btn btn-secondary">unfollow</a>
    {% else %}
        <a href="{% url 'accounts:follow' user_profile.username %}" class="btn btn-primary">follow</a>
    {% endif%}
</div>
```

## 29. feed 기능 구현
- 버튼 생성 `../templates/_nav.html`
- 경로 설정 `posts/urls.py`
- 함수 생성 `posts/views.py`
```python
def feed(request):
    followings = request.user.followings.all()
    # 현재 로그인한 사람의 팔로잉목록

    posts = Post.objects.filter(user__in=followings) 
    # 내가 팔로우하는 사람들이 작성한 게시물들

    form = CommentForm()

    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'index.html', context)
```
# JavaScript
## 30. like-async
- 좋아요 버튼을 눌렀을 때 페이지가 새로고침되는 현상 수정
- class에 like 추가, a 태그 삭제, data-post-id 추가
```html
<!-- posts/templates/_card.html -->
<i class="bi like bi-heart-fill" style="color: red;" data-post-id="{{post.id}}"></i>

<i class="bi like bi-heart" data-post-id="{{post.id}}"></i>
```
- js 적용
```html
<!-- posts/templates/index.html -->
<script>
    let likeBtns = document.querySelectorAll('i.like')
    
    let likeRequest = async (btn, postId) => {
        let likeURL = `/posts/${postId}/like-async`
        
        let res = await fetch(likeURL)
    }

    likeBtns.forEach(function(likeBtn){
        likeBtn.addEventListener('click', function(e){
            const postId = e.target.dataset.postId
            // data-post-id => dataset.postId

            likeRequest(likeBtn, postId)
        })
    })
</script>
```
- 받아줄 link 설정
```python
# posts/urls.py
path('<int:id>/like-async', views.like_async, name='like_async')
```
- 함수 설정
```python
# posts/views.py
from django.http import JsonResponse
# dict -> json

def like_async(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True
    
    context = {
        'post_id': id,
        'status': status,
    }

    return JsonResponse(context)
```
```html
<!-- posts/templates/index.html -->
<script>
    let likeRequest = async (btn, postId) => {
        let likeURL = `/posts/${postId}/like-async`
        
        let res = await fetch(likeURL)
        let result = await res.json()
        // 위에서 만든 json을 받아옴

        if (result.status) {
            btn.style.color = 'red'
            btn.classList.remove('bi-heart')
            btn.classList.add('bi-heart-fill')
        } else {
            btn.style.color = 'black'
            btn.classList.remove('bi-heart-fill')
            btn.classList.add('bi-heart')
        }
    }
<script>
```
- 좋아요 수 표시
```python
# views.py
context = {'count': len(post.like_users.all())}
```
```html
<!-- _card.html -->
{% if user in post.like_users.all %}
    <i class="bi like bi-heart-fill" style="color: red;" data-post-id="{{post.id}}">
    <span style="color: black;">{{post.like_users.all|length}}</span>
    </i>
{% else %}
    <i class="bi like bi-heart" data-post-id="{{post.id}}">
    <span style="color: black;">{{post.like_users.all|length}}</span>
    </i>
{% endif %}
<span> likes</span>
```
```js
// index.html
btn.querySelector('span').innerHTML = result.count
```

---
### commit message 수정
```shell
git commit --amend
```
- i: insert mode 설정 -> 수정
- esc: inset mode 해제
- :wq
