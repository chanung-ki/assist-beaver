from django.shortcuts import render
from share.decorators import login_required

# Create your views here.
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        pass

@login_required
def index(request):
    return render(request, 'index.html')

def raw_index(request):
    return render(request, 'raw_index.html')