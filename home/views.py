import urllib

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Views here
def index(request):
    return render(request, 'home/base_home.html')

def priceRealtime(request):
    return render(request, 'task1-price/base_1_price.html')

def tickerBlockchain(request):
    url = "https://blockchain.info/ticker"
    response = urllib.request.urlopen(url)
    return HttpResponse(response.read(), content_type="application/json")

def priceHistorical(request):
    url = "https://api.blockchain.info/charts/market-price?timespan=6months&rollingAverage=8hours&format=json"
    response = urllib.request.urlopen(url)
    return HttpResponse(response.read(), content_type="application/json")

def priceExchange(request):
    return render(request, 'task4-exchange/base_4_exchange.html')

def tickerBitfinex(request):
    url = "https://api.bitfinex.com/v1/pubticker/btcusd"
    response = urllib.request.urlopen(url)
    return HttpResponse(response.read(), content_type="application/json")

def tickerKraken(request):
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    response = urllib.request.urlopen(url)
    return HttpResponse(response.read(), content_type="application/json")

def depthKraken(request):
    url = "https://api.kraken.com/0/public/Depth?pair=XBTUSD&count=1000"
    response = urllib.request.urlopen(url)
    return HttpResponse(response.read(), content_type="application/json")
