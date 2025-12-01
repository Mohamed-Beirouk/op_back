from django.contrib import admin

from op_app.models import Categorie, ObjectPerdus

# Register your models here.
admin.site.site_header = "Lost and Found Administration"
admin.site.site_title = "Lost and Found Admin Portal"
admin.site.index_title = "Welcome to Lost and Found Admin"  


admin.site.register(Categorie)
admin.site.register(ObjectPerdus)