# insta

- 프로젝트 이름: 서비스 이름
- 모델 이름: 앱 이름

## 0. Setting
- 가상환경 생성/ 활성화
- django 설치
- .gitignore

## 1. startproject/ startapp
- 앱 등록

## 2. base.html 기본 구조
- templates 등록

## 3. Post modeling/ migration
- ImageField
```python
image = models.ImageField(upload_to='image')
# 필수 옵션 'upload_to': 이미지가 저장되는 공간
```
- makemigrations
- error
```shell
pip install pillow
```
- migrate