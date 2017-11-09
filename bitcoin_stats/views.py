from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    return render(request, "bitcoin_stats/index.html", dict())


def trace_price(request):
    return render(request, "bitcoin_stats/basic_view.html", {'topic':"Trace price"})


def compare_price(request):
    return render(request, "bitcoin_stats/basic_view.html", {'topic':"Compare price"})


def exchange_activity(request):
    return render(request, "bitcoin_stats/basic_view.html", {'topic':"Users activity on an exchange page"})


def potential_attacks(request):
    return render(request, "bitcoin_stats/basic_view.html", {'topic':"Potential attacks on the NTU's full Bitcoin node"})


def inspect_address(request):
    return render(request, "bitcoin_stats/basic_view.html", {'topic':"Inspect a Bitcoin address"})
