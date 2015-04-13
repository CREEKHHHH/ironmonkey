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
    Categories=models.ManyToManyField(FoodCategories)

    def __unicode__(self):
        return self.ItemName


class FoodItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(FoodItem,FoodItemAdmin)
class FoodCategoriesAdmin(admin.ModelAdmin):
    pass
admin.site.register(FoodCategories,FoodCategoriesAdmin)
