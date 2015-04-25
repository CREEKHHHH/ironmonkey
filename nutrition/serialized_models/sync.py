__author__ = 'sandeep.polisetty'
import httplib,urllib
from nutrition.models import FoodItem
from rest_framework.renderers import JSONRenderer
def sync():
    foodItems=FoodItem.objects.all()
    for item in foodItems:
        temp={}
        temp['_id']=item.id
        temp['name']=item.itemName
        temp['name_not_anal']=item.itemName
        temp['mfg']=item.mfgName
        temp['itemDescription']=item.itemDescription

        sugg={}
        sugg['input']=item.itemName
        pld={"id":item.id}
        sugg['payload']=pld
        temp['name_suggest']=sugg
        temp['total_cal']=item.totalCal
        temp['carb_gms']=item.carb
        temp['fat_gms']=item.fat
        temp['sugar_gms']=item.sugar
        temp['protein_gms']=item.protein

        temp['carbPerc']=item.carbPerc
        temp['fatPerc']=item.fatPerc
        temp['proteinPerc']=item.proteinPerc
        temp['sugarPerc']=item.sugarPerc

        temp['serving_size']=item.servingSize
        temp['serving_desc']=item.servingDesc
        temp['serving_gram']=item.servingGram
        rendered= JSONRenderer().render(temp)
        conn=httplib.HTTPConnection("127.0.0.1:9200")
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn.request("POST",'/food/item/'+str(item.id),rendered,headers)
        print conn.getresponse().read()
        conn.close()