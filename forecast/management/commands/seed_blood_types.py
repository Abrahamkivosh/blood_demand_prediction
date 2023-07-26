# seed_blood_types.py

from django.core.management.base import BaseCommand
from forecast.models import BloodType

class Command(BaseCommand):
    help = 'Seed the blood types in the database.'

    def handle(self, *args, **options):
        blood_types = [
            {'blood_type_name': 'A-', 'description': 'Blood Type A negative'},
            {'blood_type_name': 'A+', 'description': 'Blood Type A positive'},
            {'blood_type_name': 'B-', 'description': 'Blood Type B negative'},
            {'blood_type_name': 'B+', 'description': 'Blood Type B positive'},
            {'blood_type_name': 'AB-', 'description': 'Blood Type AB negative'},
            {'blood_type_name': 'AB+', 'description': 'Blood Type AB positive'},
            {'blood_type_name': 'O-', 'description': 'Blood Type O negative'},
            {'blood_type_name': 'O+', 'description': 'Blood Type O positive'},
        ]

        added = 0
        skipped = 0

        for blood_type_data in blood_types:
            blood_type = BloodType.objects.filter(blood_type_name=blood_type_data['blood_type_name']).first()

            if not blood_type:
                BloodType.objects.create(**blood_type_data)
                added += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {added} blood types and skipped {skipped} blood types.'))
