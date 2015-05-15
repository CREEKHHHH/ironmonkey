__author__ = 'sandeep.polisetty'
from nutrition.models import *;

HEALTHY_SNACK=2
AVOID=3
MORNING=5
BEDTIME=7
POSTWORKOUT=11
page_size=20

def getTitle(category):
    if(category==HEALTHY_SNACK):
        return "HEALTHY SNACK"
    if(category==AVOID):
        return "UNHEALTHY"
    if(category==MORNING):
        return "DAYTIME FOOD"
    if(category==BEDTIME):
        return "BEDTIME"
    if(category==POSTWORKOUT):
        return "POST-WORKOUT"

def getCatgoryResults(category,page=1):

    title=getTitle(int(category))
    query='TagValue%%'+str(category)+"=0"
    totalPages=len(FoodTag.objects.extra(where=[query]))/page_size
    fts=FoodTag.objects.extra(where=[query]).order_by('id')[(page-1)*page_size:page*page_size]
    print fts
    rs=[]
    for ft in fts:
        rs.append(FoodItem.objects.get(id=ft.id))
    return {'results':rs,'cat':title,'totalPages':totalPages,'curr_page':page}
