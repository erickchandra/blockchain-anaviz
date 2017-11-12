import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Views here
def index(request):
    return render(request, 'home/base_home.html')

def priceRealtime(request):
    return render(request, 'task1-price/base_1_price.html')

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
