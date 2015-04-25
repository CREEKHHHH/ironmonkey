from django.db import models
from django.contrib import admin

# Create your models here.

'''
class FoodCategories(models.Model):
    id=models.AutoField(primary_key=True)
    CategoryName=models.CharField(max_length=30,unique=True)
    def __unicode__(self):
        return self.CategoryName
'''
class FoodItem(models.Model):
    id=models.AutoField(primary_key=True)

    itemName=models.CharField(max_length=100,null=True)
    mfgName=models.CharField(max_length=100,null=True)
    itemDescription=models.CharField(max_length=200,null=True)
    imgUrl=models.CharField(max_length=200,null=True)
    url=models.CharField(max_length=200,null=True)


    totalCal=models.FloatField(null=True)
    carb=models.FloatField(null=True)
    fat=models.FloatField(null=True)
    sugar=models.FloatField(null=True)
    protein=models.FloatField(null=True)

    servingSize=models.CharField(null=True,max_length=50)
    servingDesc=models.CharField(max_length=100,null=True)
    servingGram=models.FloatField()


    sugarPerc=models.FloatField(editable=False,null=True)
    carbPerc=models.FloatField(editable=False,null=True)
    fatPerc=models.FloatField(editable=False,null=True)
    proteinPerc=models.FloatField(editable=False,null=True)

    #    Categories=models.ManyToManyField(FoodCategories)

    def save(self):
        t=self.totalCal
        self.carbPerc=0
        self.fatPerc=0
        self.proteinPerc=0
        self.sugarPerc=0
        if(t!=0):
            if self.carb !=None:self.carbPerc=4*(self.carb/t)*100
            if self.sugar!=None: self.sugarPerc=4*(self.sugar/t)*100
            if self.fat!=None: self.fatPerc=8*(self.fat/t)*100
            if self.protein!=None: self.proteinPerc=4*(self.protein/t)*100
        super(FoodItem,self).save()






    def __unicode__(self):
        return self.itemName


class FoodItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(FoodItem,FoodItemAdmin)
'''
class FoodCategoriesAdmin(admin.ModelAdmin):
    pass
admin.site.register(FoodCategories,FoodCategoriesAdmin)
'''