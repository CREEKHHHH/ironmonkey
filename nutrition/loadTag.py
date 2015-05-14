__author__ = 'sandeep.polisetty'

from nutrition.models import FoodItem,FoodTag
from nutrition.tagConstants import *
def getTagValue( fi):
   c=fi.carbPerc
   f=fi.fatPerc
   p=fi.proteinPerc
   s=fi.sugarPerc
   rt=1
   if(p<20 and f>30 and f<70):
       rt=rt*AVOID
       return rt
   if p>20 and ( f<15 or c<15) and s<10:
       rt=rt*HEALTHY_SNACK
   if f<20 and c >20 and s<20:
       rt=rt*MORNING
   if c<20:
       rt=rt*BEDTIME
   if s>20 and f<15:
       rt=rt*POSTWORKOUT
   return rt


def updateTag():
    for fi in  FoodItem.objects.all() :
        tg=getTagValue(fi)
        a=FoodTag()
        a.id=fi.id
        a.tagValue=tg
        a.save()