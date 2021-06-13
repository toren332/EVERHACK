from django.core.management.base import BaseCommand
from service.models import Building
import random
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point, MultiPoint


gcoord = SpatialReference(4326)
mycoord = SpatialReference(3857)
trans1 = CoordTransform(gcoord, mycoord)
trans2 = CoordTransform(mycoord, gcoord)


def combine_geoobjects_to_geojson(*args):
    GJS = '''{"type": "FeatureCollection","features": ['''
    for obj in args[:-1]:
        GJS += f'''{{"type": "Feature","geometry": {obj.geojson},"properties": {{}} }},'''
    GJS += f'''{{"type": "Feature","geometry": {args[-1].geojson},"properties": {{}} }}'''
    GJS += ''']}'''
    return GJS


def get_random_char():
    return random.choice('abcdefghijklmnopqrstuvwxyz')


def get_random_points_form_polygon(polygon, num_points=100):
    env = polygon.ogr.envelope
    xmin, ymin, xmax, ymax = env.min_x,env.min_y,env.max_x,env.max_y

    points = set()
    while len(points) < num_points:
        point = Point(random.uniform(xmin, xmax), random.uniform(ymin, ymax))
        if point.intersection(polygon):
            points.add(point)
    return list(points)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_count = 50
        Building.objects.all().delete()
        point = Point(37.620407, 55.754093, srid=4326)
        point.transform(trans1)
        point_buffer = point.buffer(50000)
        point_buffer.transform(trans2)
        points = get_random_points_form_polygon(point_buffer, num_points=users_count)
        building_models = []
        print(combine_geoobjects_to_geojson(point_buffer, *points))
        for i in range(users_count):
            # Building.objects.create(point=point)
            building = Building()
            building.point = points[i]

            building_models.append(building)
        Building.objects.bulk_create(building_models, batch_size=10000)
