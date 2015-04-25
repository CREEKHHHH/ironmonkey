# Create your views here.
from django.shortcuts import render_to_response
from nutrition.es import *
maxPageShown=7
def replaceFoodItem(request):
    if request.GET.has_key('id') and request.GET['id']!="":
        id=int(request.GET['id'])
    else:
        return searchFoodItem()
    results_dict={}
    if request.GET.has_key('pageNo') and request.GET['pageNo']!="":
        pageNo=int(request.GET['pageNo'])
        results_dict=getViableReplacementResultsForId(id,pageNo)
    else:
        results_dict=getViableReplacementResultsForId(id)
    print results_dict
    results_dict['root_url']='replace/'
    if results_dict['totalPages']>maxPageShown:
        results_dict['totalPages']=maxPageShown
    results_dict['totalPageRange']=range(1,results_dict['totalPages'])
    results_dict['url']="id="+str(id)
    return render_to_response('replace.html',results_dict)

def searchFoodItem(request):
    if request.GET.has_key("id") and request.GET["id"]!="":
        id=int(request.GET['id'])
        results_dict=getESResultsForIdSearch(id)
        results_dict['url']="id="+str(id)
        return render_to_response('search.html',results_dict)
    if request.GET.has_key('pageNo'):
        pageNo=int(request.GET['pageNo'])
    else:
        pageNo=1
    if (request.GET.has_key('text')) and request.GET["text"]!="":
        text=request.GET['text']
    else:
        text=None
    results_dict=getESResultsForTextSearch(text,pageNo)
    if text !=None :
        results_dict['url']="text="+str(text)
    else:
        results_dict['url']="text="
    print results_dict['totalPages']
    if results_dict['totalPages']>maxPageShown:
        results_dict['totalPages']=maxPageShown
    results_dict['totalPageRange']=range(1,results_dict['totalPages'])
    return render_to_response('search.html',results_dict)