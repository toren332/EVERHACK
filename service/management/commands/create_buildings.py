import json

from django.core.management.base import BaseCommand
from service.models import Building
import random
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point, MultiPoint
import csv
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        # _ = 0
        Building.objects.all().delete()
        building_models = []
        with open('реальные точки КН.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                point = Point((float(row['X']), float(row['Y'])), srid=4326)
                sell_type = row['sell_type']
                square = row['square']
                kind = row['kind']
                total_price = row['total_price']
                # image = json.loads(row['images'])['orig']
                image = "https://65.img.avito.st/image/1/oNLn4bayDDvRSM4-q6OApgVCDD1HQA4"

                # if not os.path.isfile(image):
                #     _+=1
                # # print( )
                #     print(image)
                building = Building(point=point, sell_type=sell_type, square=square, kind=kind, total_price=total_price, image=image)
                building_models.append(building)
        Building.objects.bulk_create(building_models, batch_size=10000)
        # print(_)
#2276
#1972