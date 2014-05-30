from django.db import models

# Create your models here.

class Element(models.Model):
    structural_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    description = models.TextField()
    email = models.CharField(max_length=200)
    phone1 = models.CharField(max_length=30)




