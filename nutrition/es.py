__author__ = 'sandeep.polisetty'
import httplib,urllib,json
from django.conf import  settings
from rest_framework.renderers import JSONRenderer
from  nutrition.serialized_models.foodItemDTO import getListOfFoodItemDTO
import pprint

headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
ES_URL=settings.ES_URL
defaultPgNo=1
defaultSizeNo=10
replacmentMargin=10

def getESResultsForTextSearch(text=None,pageNo=defaultPgNo,size=defaultSizeNo):
    if text==None:
        return getESResultsForAll(pageNo,size)
    conn=httplib.HTTPConnection(ES_URL)
    url='/food/item/_search'
    params={"query":{"fuzzy":{"name":{"value":text,"fuzziness":2.0}}}}
    params['from']=((pageNo)-1)*size
    params['size']=size
    rendered=JSONRenderer().render(params)
    conn.request("POST",url,rendered,headers)
    response=conn.getresponse().read()
    data=getListOfFoodItemDTO(json.loads(response))
    conn.close()
    data['totalPages']=int(data['hits']/size)
    data['curr_page']=pageNo
    return data


def getESResultsForIdSearch(id=None):
    conn=httplib.HTTPConnection(ES_URL)
    if id==None:
        getESResultsForAll()
    url='/food/item/_search'
    params={'query':{
            "filtered":{
                "filter":{"term":{"_id":id}},
                "query":{'match_all':{}}
                }}}
    rendered=JSONRenderer().render(params)
    conn.request("POST",url=url,headers=headers,body=rendered)
    response=conn.getresponse().read()
    data=getListOfFoodItemDTO(json.loads(response))
    conn.close()
    data['totalPages']=1
    data['curr_page']=1
    return data


def getESResultsForAll(pageNo=defaultPgNo,size=defaultSizeNo):
    conn=httplib.HTTPConnection(ES_URL)
    url='/food/item/_search'
    params={'query':{'match_all':{}}}
    params['from']=((pageNo)-1)*size
    params['size']=size
    rendered=JSONRenderer().render(params)
    conn.request("POST",url,rendered,headers)
    response=conn.getresponse().read()
    data=getListOfFoodItemDTO(json.loads(response))
    data['totalPages']=int(data['hits']/size)
    data['curr_page']=pageNo
    conn.close()
    return data

def getESResultsForViableReplacement(carbPerc,proteinPerc,fatPerc,sugarPerc,pageNo=defaultPgNo,size=defaultSizeNo):
    carbRng={'range':{'carbPerc':{"lte":(carbPerc+replacmentMargin),"gte":(carbPerc-replacmentMargin)}}}
    fatRng={'range':{'fatPerc':{"lte":(fatPerc+replacmentMargin),"gte":(fatPerc-replacmentMargin)}}}
    proteinRng={'range':{'proteinPerc':{"lte":(proteinPerc+replacmentMargin),"gte":(proteinPerc-replacmentMargin)}}}
    sugarRng={'range':{'sugarPerc':{"lte":(sugarPerc+replacmentMargin),"gte":(sugarPerc-replacmentMargin)}}}
    query={"function_score":{"functions":[
		{"linear":{
		"carbPerc":{
		"origin":carbPerc,
		"scale":1}}}
    ,	{"linear":{
		"fatPerc":{
		"origin":fatPerc,
		"scale":1}}}
    ,	{"linear":{
		"sugarPerc":{
		"origin":sugarPerc,
		"scale":1}}}
    ,	{"linear":{
		"proteinPerc":{
		"origin":proteinPerc,
		"scale":1}}}
    ],
		"query": {
          "match_all": {}
        }}
}
    params={'query':{'filtered':{
        "filter":{"and":[carbRng,fatRng,proteinRng,sugarRng]},'query':query
    }}}

    '''params={'query':{'filtered':{
        "filter":{"and":[carbRng,fatRng,proteinRng,sugarRng]},'query':{'match_all':{}}
    }}}'''
    params['from']=((pageNo)-1)*size
    params['size']=size
    rendered=JSONRenderer().render(params)
    conn=httplib.HTTPConnection(ES_URL)
    url='/food/item/_search'
    conn.request("POST",url,rendered,headers)
    response=conn.getresponse().read()
    data=getListOfFoodItemDTO(json.loads(response))
    conn.close()
    return data

def getViableReplacementResultsForId(id,pageNo=defaultPgNo,size=defaultSizeNo):
    itm=getESResultsForIdSearch(id)
    if len(itm['results'])==0:
        return {}
    itmDTO=itm['results'][0]
    dict_results=getESResultsForViableReplacement(int(itmDTO.carbPerc),int(itmDTO.proteinPerc),int(itmDTO.fatPerc),int(itmDTO.sugarPerc),pageNo,size)
    for ech in dict_results['results']:
        ech.replacement=int((ech.totalCal*ech.serving_gram)/itmDTO.totalCal)
    dict_results['selectedItem']=itmDTO
    dict_results['totalPages']=int(dict_results['hits']/size)
    dict_results['curr_page']=pageNo
    dict_results['totalPageRange']=range(1,dict_results['totalPages'])
    return dict_results


#getESResultsForViableReplacement(10,10,10,10)