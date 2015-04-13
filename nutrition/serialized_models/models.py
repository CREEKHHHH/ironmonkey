__author__ = 'sandeep.polisetty'
from rest_framework import serializers
from nutrition.models import FoodItem,FoodCategories
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodCategories
        fields=('id','CategoryName')

class FoodItemSerializer(serializers.ModelSerializer):
    Categories=CategoriesSerializer(many=True)
    class Meta:
        model=FoodItem
        fields=( 'id', 'ItemName','TotalCal','Carb','Fat','Protein','Categories')