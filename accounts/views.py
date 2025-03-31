from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():

            # user 정보 가져오기
            user = form.get_user()

            # login 처리 -> session 만들기
            auth_login(request, user)

            return redirect('posts:index')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)