from django.db import models
from django.utils import timezone
class BloodType(models.Model):
    BLOOD_TYPE_NAME = (
            ('A-', 'A-'),
            ('A+', 'A+'),
            ('B-', 'B-'),
            ('B+', 'B+'),
            ('AB-', 'AB-'),
            ('AB+', 'AB+'),
            ('O-', 'O-'),
            ('O+', 'O+'),


        )

    blood_type_name = models.CharField(max_length=3, choices=BLOOD_TYPE_NAME)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.blood_type_name
    
class Location(models.Model):
    name = models.CharField(max_length=250)
    population = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class BloodDemandPrediction(models.Model):
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    date = models.DateField(  blank=True, null=True)
    predicted_demand = models.FloatField()
    age = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    events = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"{self.blood_type} - {self.date}"
    


class BloodSupply(models.Model):
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    date = models.DateField()
    blood_quantity = models.FloatField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    blood_demand_prediction = models.ForeignKey(BloodDemandPrediction, on_delete=models.CASCADE, blank=True, null=True)
   

    def __str__(self):
        return f"{self.blood_type} - {self.date}"

