from django.core.management.base import BaseCommand
from forecast.models import BloodSupply, BloodDemandPrediction, WeatherForecast

class Command(BaseCommand):

    help = 'Delete all data in specified models'

    def handle(self, *args, **kwargs):
        # Call the delete_all_data_in_model function for each model
        self.delete_all_data_in_model(BloodSupply)
        self.delete_all_data_in_model(BloodDemandPrediction)
        self.delete_all_data_in_model(WeatherForecast)

        self.stdout.write(self.style.SUCCESS(f'Successfully Deleted All , BloodSupply, BloodDemandPrediction, WeatherForecast '))

    def delete_all_data_in_model(self, model):
        model.objects.all().delete()