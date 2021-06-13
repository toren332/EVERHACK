from django.core.management.base import BaseCommand
from service.models import Building, Poly
import random
import csv
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point, MultiPoint
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
import json

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
    "business": "winter",
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        D = {}
        norm = mpl.colors.Normalize(vmin=0, vmax=100)
        for k, v in MATCH_DICT.items():
            D[k] = [rgb2hex(cm.ScalarMappable(norm=norm, cmap=cm.get_cmap(MATCH_DICT[k])).to_rgba(float(0.01))),
                    rgb2hex(cm.ScalarMappable(norm=norm, cmap=cm.get_cmap(MATCH_DICT[k])).to_rgba(float(99.99)))]
        # print(D)
        with open('cmaps.json', 'w') as f:
            json.dump(D, f, indent=4)
        Poly.objects.all().delete()
        poly_models = []
        with open('cells (1).csv') as csvfile:
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
