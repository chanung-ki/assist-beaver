from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from share.decorators import login_required, not_allow_login, admin_only

def signin_view(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is None:
        msg = '잘못된 이메일 혹은 비밀번호 입니다.'
        messages.add_message(request, messages.ERROR, msg)
        return redirect('signin_view')
        
    login(request, user)
    return redirect('index')


def signout_view(request):
    logout(request)
    msg = '로그아웃이 완료 되었습니다.'
    messages.add_message(request, messages.SUCCESS, msg)
    return redirect('signin_view')
        

@login_required
def index(request):
    return render(request, 'index.html')

@admin_only
def raw_index(request):
    return render(request, 'raw_index.html')
