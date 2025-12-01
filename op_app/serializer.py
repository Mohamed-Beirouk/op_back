from rest_framework import serializers
from django.contrib.auth.models import User   
from .models import Categorie, ObjectPerdus  



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']



class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'name']



class ObjectPerdusSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = ObjectPerdus
        fields = ['id', 'title', 'description', 'date_found','location_found', 'category', 'found_by', 'status', 'image']