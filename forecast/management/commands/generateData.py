import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path
from django.core.management.base import BaseCommand


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def generateTheData():
    # Set random seed for reproducibility
    np.random.seed(42)

    fake = Faker()

    start_date = datetime(2020, 1, 1)
    end_date = datetime(2020, 12, 31)
    num_days = (end_date - start_date).days + 1

    data = []

    for _ in range(num_days):
        date = start_date + timedelta(days=np.random.randint(num_days))  # Unique date
        blood_demand = np.random.randint(0, 100)  # Hypothetical blood demand formula
        temperature = round(np.random.uniform(30, 40), 2)
        age_distribution = np.random.randint(18, 80)
        population = np.random.randint(100000, 1000000)
        events = np.random.randint(0, 2)
        
        for gender in ["Male", "Female"]:
            blood_type = fake.random_element(elements=("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"))
            
            data.append([date, blood_demand, temperature, blood_type, age_distribution, gender, population, events])

    # Create a DataFrame
    columns = ["Date", "Blood Demand", "Temperature (°C)", "Blood Type", "Age", "Gender", "Population", "Events"]
    df = pd.DataFrame(data, columns=columns)

    # Save to CSV
    path_to_data = BASE_DIR / "data"
    df.to_csv(path_to_data / "blood_demand_data_2020.csv", index=False)


class Command(BaseCommand):
    
        help = 'Generate data for blood demand'
    
        def handle(self, *args, **kwargs):
            generateTheData()
            self.stdout.write(self.style.SUCCESS(f'Successfully Generated Data for Blood Demand'))