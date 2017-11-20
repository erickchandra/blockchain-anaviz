import urllib
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.staticfiles.finders import find
from django import forms

import home.node_connection

# Views here
from home import node_connection


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

def userBehaviour(request):
    url = find("user_behaviour/dummy.json")

    user_behaviours = {}
    with open(url) as json_data:
        data = json.load(json_data)
        for item in data:
            timestamp = int(float(item["timestamp"]))
            if timestamp in user_behaviours:
                user_behaviours[timestamp] += 1
            else:
                user_behaviours[timestamp] = 1
    return render(request, 'task2-user-behaviour/user_behaviour.html', context={'user_behaviours': json.dumps(user_behaviours)})


class AddressTraceRequestForm(forms.Form):
    addressToTrace = forms.CharField(label="Address to trace:", max_length=34, min_length=26)
    numberOfBlocks = forms.IntegerField(label="Number of top blocks to search:", initial=3)

def addresTracerRequest(request):
    node_connection.start()
    if request.method == 'GET':
        print("jestem")
        form = AddressTraceRequestForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            print(data['addressToTrace'], data['numberOfBlocks'])
            received_from, send_to = node_connection.analize_chain(data['addressToTrace'], data['numberOfBlocks'])
            send_to = list(send_to)
            received_from = list(received_from)
            data["sent_to"] = send_to
            data["received_from"] = received_from
            return render(request, "task5-address-tracer/display.html", context=form.cleaned_data)
    else:
        form = AddressTraceRequestForm()
    return render(request, "task5-address-tracer/form.html", context=({"form": form}))




