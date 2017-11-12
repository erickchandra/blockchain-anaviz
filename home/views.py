import urllib

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Views here
def index(request):
    return render(request, 'home/base_home.html')

def priceRealtime(request):
    return render(request, 'task1-price/base_1_price.html')

def priceHistorical(request):
    url = "https://api.blockchain.info/charts/market-price?timespan=6months&rollingAverage=8hours&format=json"
    response = urllib.request.urlopen(url)
    return HttpResponse(response.read(), content_type="application/json")
