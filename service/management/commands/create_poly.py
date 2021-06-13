from django.core.management.base import BaseCommand
from service.models import Building, Poly
import random
import csv
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point, MultiPoint
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex

MATCH_DICT = {
    "supermarket": "viridis",
    "alco": "cividis",
    "restaurant": "Blues",
    "cafe": "Reds",
    "pubs": "PuBu",
    "night_club": "RdPu",
    "fast_food": "Oranges",
    "coffee": "GnBu",
    "hospital": "YlGn",
    "clinic": "binary",
    "dentist": "Wistia",
    "vet": "copper",
    "food_retail": "hot",
    "beauty":  "cool",
    "horeca": "spring",
    "healthcare": "autumn",
    "other": "plasma",
    "bussines": "winter",
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        norm = mpl.colors.Normalize(vmin=0, vmax=100)
        Poly.objects.all().delete()
        poly_models = []
        with open('пример полигонов.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                polygon = row['geometry']
                rank = row['Rank']
                business_kind = row['Kind']
                color = rgb2hex(cm.ScalarMappable(norm=norm, cmap=cm.get_cmap(MATCH_DICT[business_kind])).to_rgba(float(rank)))
                # print(color)
                poly = Poly(polygon=polygon, rank=rank, business_kind=business_kind, fill=color)
                poly_models.append(poly)
        Poly.objects.bulk_create(poly_models, batch_size=10000)
