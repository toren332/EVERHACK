from django.db import models
from django.contrib.gis.db import models as gis_models


class Building(models.Model):
    point = gis_models.PointField()
    kind = models.CharField(max_length=128)
    sell_type = models.CharField(max_length=128)
    total_price = models.FloatField()
    square = models.FloatField()
    image = models.URLField(blank=True, null=True)
    first_line = models.BooleanField(default=False)


class Poly(models.Model):
    polygon = gis_models.PolygonField()
    rank = models.FloatField()
    fill = models.CharField(max_length=10)
    business_kind = models.CharField(max_length=64)
