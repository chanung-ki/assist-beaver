from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed

# Create your views here.
def shipping(request):
    return render(request, 'shipping.html')

def table(request):
    return render(request, 'table.html')

def separate_address(request):
    
    if not request.method == "POST":
        return HttpResponseNotAllowed(['POST'])
    
    uploaded_file = request.FILES.get('addressFile')
    
    print(uploaded_file)

    return redirect('msk_shipping')
    
    
