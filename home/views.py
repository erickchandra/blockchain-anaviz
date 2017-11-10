from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Views here
def index(request):
    return render(request, 'home/base_home.html')

def priceRealtime(request):
    return render(request, 'task1-price/base_1_price.html')
