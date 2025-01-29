from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            msg = '로그인 후 이용해주세요.'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('signin')
        return view_func(request, *args, **kwargs)
    return wrapper



def not_allow_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper