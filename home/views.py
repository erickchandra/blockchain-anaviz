from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader

# Views here
def index(request):
    return render(request, 'home/index.html', dict())
    # return render_to_response('admin-lte/index2.html')
