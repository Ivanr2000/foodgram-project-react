import csv
import os

from django.core.management.base import BaseCommand

from foodgram_project.settings import BASE_DIR
from recipes.models import Ingredient, UnitOfMeasurement

path_to_data = ''

TABLES = {
    Ingredient: 'ingredients.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fieldnames = ['name', 'measurement_unit']
        for model, csv_f in TABLES.items():
            with open(
                os.path.join(BASE_DIR, path_to_data, csv_f),
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                for data in reader:
                    _, created = Ingredient.objects.get_or_create(
                        name=data['name'],
                        measurement_unit=(
                            UnitOfMeasurement.objects.get_or_create(
                                name=data['measurement_unit'])[0]
                        ),
                    )
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
