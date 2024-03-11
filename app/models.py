from django.db import models

# Create your models here.
class Farmer(models.Model):
    phone_number= models.CharField(max_length=15, unique=True)
    name=models.CharField(max_length=255)
    language=models.CharField(max_length=50)
    

class Farm(models.Model):
    farmer=models.ForeignKey(Farmer, on_delete=models.CASCADE)
    area=models.FloatField()
    village=models.CharField(max_length=255)
    crop_grown=models.CharField(max_length=100)
    sowing_date= models.DateField()
    
class Schedule(models.Model):
    farm=models.ForeignKey(Farm, on_delete= models.CASCADE)
    days_after_sowing = models.PositiveIntegerField()
    fertiliser = models.FloatField(max_length=100)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=10)
    
    