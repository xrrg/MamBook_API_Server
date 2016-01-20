from django.shortcuts import render

# Create your views here.


def initialize(request):
    context = dict()

    return render(request, '', context)
