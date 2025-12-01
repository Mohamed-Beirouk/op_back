from django.db import models
from django.contrib.auth.models import User


class Categorie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class ObjectPerdus(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_found = models.DateField()
    location_found = models.CharField(max_length=200)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    found_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('found', 'Found'), ('returned', 'Returned')], default='found')
    image = models.ImageField(upload_to='static/object_images/', null=True, blank=True)
    def __str__(self):
        return self.title