import urllib
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.staticfiles.finders import find

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

def tracing(request):
    # access = ServiceProxy("http://2b:hw234@140.112.29.42:8332")
    # print (access.getinfo())
    url = find("tracing/dummy.json")
    with open(url) as json_data:
        data = json.load(json_data)

        arcs = []

        for item in data:
            arc = {}

            arc["origin"] = {
                "latitude": 25.0418,
                "longitude": 121.4966
            }

            ip_address = item["addr"].split(":")[0]
            result = urllib.request.urlopen("http://www.freegeoip.net/json/{0}".format(ip_address)).read()
            location_info = json.loads(result.decode("utf-8"))

            arc["destination"] = {
                "latitude": location_info["latitude"],
                "longitude": location_info["longitude"]
            }

            arcs.append(arc)
    return render(request, 'task5-tracing/base_5_tracing.html', context={'arcs': json.dumps(arcs)})
