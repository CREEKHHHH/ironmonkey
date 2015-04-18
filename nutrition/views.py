# Create your views here.
from django.shortcuts import render_to_response
def random(request):
    return render_to_response('search.html')