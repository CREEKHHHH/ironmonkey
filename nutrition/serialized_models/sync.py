__author__ = 'sandeep.polisetty'
import httplib,urllib
from nutrition.models import FoodItem
from rest_framework.renderers import JSONRenderer
def sync():
    foodItems=FoodItem.objects.all()
    for item in foodItems:
        temp={}
        temp['_id']=item.id
        temp['name']=item.ItemName
        temp['name_not_anal']=item.ItemName
        sugg={}
        sugg['input']=item.ItemName
        pld={"id":item.id}
        sugg['payload']=pld
        temp['name_suggest']=sugg
        temp['total_cal']=item.TotalCal
        temp['carb_gms']=item.Carb
        temp['fat_gms']=item.Fat
        temp['protein_gms']=item.Protein
        ls=[]
        for cat in item.Categories.all():
            ls.append(cat.CategoryName)
        temp['categories']=ls
        rendered= JSONRenderer().render(temp)
        conn=httplib.HTTPConnection("127.0.0.1:9200")
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn.request("POST",'/food/item/'+str(item.id),rendered,headers)
        print conn.getresponse().read()
        conn.close()