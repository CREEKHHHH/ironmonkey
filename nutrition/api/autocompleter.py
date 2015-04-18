__author__ = 'sandeep.polisetty'
import httplib,json
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
pageSize=4


@api_view(['GET'])
def searchAPI(request):
    text=request.GET['txt']
    pageNo=request.GET['pageNo']
    conn=httplib.HTTPConnection("127.0.0.1:9200")
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    url='/food/item/_search?q='+text+'&from='+str(pageNo)+'&size='+str(pageSize)
    conn.request("GET",url)
    resp=conn.getresponse().read()
    resp=json.loads(resp)
    return HttpResponse(json.dumps(resp),content_type='application/json')












def parseAutoCompResponse(response):
    response=json.loads(response)
    pld=response["name_suggest"][0]["options"]
    respDict=[]
    for ech in pld:
        temp={}
        temp["id"]=ech["payload"]["id"]
        temp["view"]=ech["text"]
        respDict.append(temp)
    return respDict

def getDictionaryForAutoComplete():
    inner1={}
    inner1["text"]=''
    inner1["completion"]={'field':'name_suggest'}
    outer={}
    outer["name_suggest"]=inner1
    return outer

@api_view(['GET'])
def autocomplete(request):
    txt=request.GET['txt']
    autoCompObj=getDictionaryForAutoComplete()
    autoCompObj["name_suggest"]["text"]=txt
    rendered= JSONRenderer().render(autoCompObj)
    conn=httplib.HTTPConnection("127.0.0.1:9200")
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn.request("POST",'/food/_suggest/',rendered,headers)
    resp=conn.getresponse().read()
    resp=parseAutoCompResponse(resp)
    return HttpResponse(json.dumps(resp),content_type='application/json')
