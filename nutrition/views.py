# Create your views here.
from django.shortcuts import render_to_response
from nutrition.api.autocompleter import searchAPI
from  nutrition.serialized_models.foodItemDTO import getListOfFoodItemDTO
import json
import httplib
def random(request):
    return render_to_response('search.html')


def searchFoodItem(request):
    #text="whole"
    if (request.GET.has_key('text')):
        text=request.GET['text']
        text=text.replace(" ","%20")
    else:
        text="wh"
    pageNo=1
    pageSize=10
    conn=httplib.HTTPConnection("127.0.0.1:9200")
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    url='/food/item/_search?q='+text+'&from='+str(pageNo)+'&size='+str(pageSize)
    conn.request("GET",url)
    resp=conn.getresponse().read()
    data=getListOfFoodItemDTO(json.loads(resp))
    #data=json.loads(resp)

    return render_to_response('search.html',{'data':data})