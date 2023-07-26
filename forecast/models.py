from django.db import models
    
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
# models.py


from django.db import models



    


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

class WeatherForecast(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)  # Latitude of the location
    longitude = models.FloatField(blank=True, null=True)  # Longitude of the location
    temperature = models.FloatField()
    humidity = models.FloatField(blank=True, null=True)
    population= models.FloatField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location} - {self.date}"


class BloodDemandPrediction(models.Model):
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    weather_forecast = models.ForeignKey(WeatherForecast, on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateField()
    predicted_demand = models.FloatField()

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