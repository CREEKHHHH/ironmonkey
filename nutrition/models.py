from django.db import models
from django.contrib import admin

# Create your models here.

class FoodCategories(models.Model):
    id=models.AutoField(primary_key=True)
    CategoryName=models.CharField(max_length=30,unique=True)
    def __unicode__(self):
        return self.CategoryName

class FoodItem(models.Model):
    id=models.AutoField(primary_key=True)
    ItemName=models.CharField(max_length=100)
    TotalCal=models.FloatField()
    Carb=models.FloatField()
    Fat=models.FloatField()
    Protein=models.FloatField()
    carbPerc=models.FloatField(editable=False)
    fatPerc=models.FloatField(editable=False)
    proteinPerc=models.FloatField(editable=False)
    servingSize=models.FloatField()
    servingUnits=models.CharField(max_length=100)
    Categories=models.ManyToManyField(FoodCategories)

    def save(self):
        t=self.Carb+self.Protein+self.Fat*2
        self.carbPerc=(self.Carb/t)*100
        self.fatPerc=(self.Fat/t)*100
        self.proteinPerc=(self.Carb/t)*100
        super(FoodItem,self).save()






    def __unicode__(self):
        return self.ItemName


class FoodItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(FoodItem,FoodItemAdmin)
class FoodCategoriesAdmin(admin.ModelAdmin):
    pass
admin.site.register(FoodCategories,FoodCategoriesAdmin)
