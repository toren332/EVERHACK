from . import serializers
from . import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.gis.geos import Polygon
from django.core.serializers import serialize
from rest_framework.response import Response
import json
from django.core.cache import cache


MATCH_DICT = {
    "food_retail": {
        "supermarket": [
            "Торговое помещение",
            "Помещение свободного назначения",
        ],
        "alco": [
            "Торговое помещение",
            "Помещение свободного назначения",
        ],
    },
    "beauty":  {
        "beauty": [
            "Помещение свободного назначения",
        ]
    },
    "horeca": {
        "restaurant": [
            "Помещение свободного назначения",
            "Помещение общественного питания",
        ],
        "cafe": [
            "Помещение свободного назначения",
            "Помещение общественного питания",
        ],
        "pubs": [
            "Помещение свободного назначения",
            "Помещение общественного питания",
        ],
        "night_club": [
            "Помещение свободного назначения",
        ],
        "fast_food": [
            "Помещение свободного назначения",
            "Помещение общественного питания",
        ],
        "coffee": [
            "Помещение свободного назначения",
            "Помещение общественного питания",
        ],
    },
    "healthcare": {
        "hospital": [
            "Помещение свободного назначения",
        ],
        "clinic": [
            "Помещение свободного назначения",
        ],
        "dentist": [
            "Помещение свободного назначения",
        ],
        "vet": [
            "Помещение свободного назначения",
        ],
    },
    "other": {
        "other": [
            "Помещение свободного назначения",
            "Торговое помещение"
        ]
    },
    "business": {
        "business": [
            "Офисное помещение"
        ]
    },
}
MATCH_DICT2 = {
    "supermarket": [
        "Торговое помещение",
        "Помещение свободного назначения",
    ],
    "alco": [
        "Торговое помещение",
        "Помещение свободного назначения",
    ],
    "beauty": [
        "Помещение свободного назначения",
    ],
    "restaurant": [
        "Помещение свободного назначения",
        "Помещение общественного питания",
    ],
    "cafe": [
        "Помещение свободного назначения",
        "Помещение общественного питания",
    ],
    "pubs": [
        "Помещение свободного назначения",
        "Помещение общественного питания",
    ],
    "night_club": [
        "Помещение свободного назначения",
    ],
    "fast_food": [
        "Помещение свободного назначения",
        "Помещение общественного питания",
    ],
    "coffee": [
        "Помещение свободного назначения",
        "Помещение общественного питания",
    ],
    "hospital": [
        "Помещение свободного назначения",
    ],
    "clinic": [
        "Помещение свободного назначения",
    ],
    "dentist": [
        "Помещение свободного назначения",
    ],
    "vet": [
        "Помещение свободного назначения",
    ],
    "other": [
        "Помещение свободного назначения",
        "Торговое помещение"
    ],
    "business": [
        "Офисное помещение"
    ]
}


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BuildingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        lat_min = self.request.GET.get('lat_min')
        lat_max = self.request.GET.get('lat_max')
        lon_min = self.request.GET.get('lon_min')
        lon_max = self.request.GET.get('lon_max')
        qs = models.Building.objects.all()
        business_kind = self.request.GET.get('business_kind')
        first_line = self.request.GET.get('first_line')
        if business_kind is not None:
            kn_s = list(MATCH_DICT2[business_kind])
            qs = qs.filter(kind__in=kn_s)
        if first_line is not None:
            qs = qs.filter(first_line=first_line)
        if None in [lat_max, lat_min, lon_min, lon_max]:
            return qs
        lat_min = float(lat_min)
        lat_max = float(lat_max)
        lon_min = float(lon_min)
        lon_max = float(lon_max)
        poly = Polygon(((lat_min, lon_min), (lat_max, lon_min), (lat_max, lon_max), (lat_min, lon_max), (lat_min, lon_min)), srid=4326)
        qs = qs.filter(point__intersects=poly)
        return qs

    def list(self, request, *args, **kwargs):
        # d = cache.get('buildings')
        d = None
        if d is None:
            queryset = self.filter_queryset(self.get_queryset())
            d = json.loads(serialize('geojson', queryset,
              geometry_field='point',
              fields=('id', 'kind', 'sell_type', 'total_price', 'square', 'image', 'first_line')))
            # cache.set('buildings', d, 60*60*24)
        resp = Response(d)
        resp["Access-Control-Allow-Origin"] = '*'
        resp["Access-Control-Allow-Methods"] = 'GET,PUT, OPTIONS'
        resp["Access-Control-Max-Age"] = '1000'
        resp["Access-Control-Allow-Headers"] = 'X-Requested-With, Content-Type'
        return resp




class PolyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PolySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        lat_min = self.request.GET.get('lat_min')
        lat_max = self.request.GET.get('lat_max')
        lon_min = self.request.GET.get('lon_min')
        lon_max = self.request.GET.get('lon_max')
        business_kind = self.request.GET.get('business_kind')
        qs = models.Poly.objects.all()
        if business_kind is not None:
            qs = qs.filter(business_kind=business_kind)
        if None in [lat_max, lat_min, lon_min, lon_max]:
            return qs
        lat_min = float(lat_min)
        lat_max = float(lat_max)
        lon_min = float(lon_min)
        lon_max = float(lon_max)
        poly = Polygon(((lat_min, lon_min), (lat_max, lon_min), (lat_max, lon_max), (lat_min, lon_max), (lat_min, lon_min)), srid=4326)
        qs = qs.filter(polygon__intersects=poly)
        return qs

    def list(self, request, *args, **kwargs):
        # d = cache.get('poly')
        d = None
        if d is None:
            queryset = self.filter_queryset(self.get_queryset())
            d = json.loads(serialize('geojson', queryset,
              geometry_field='polygon',
              fields=('id', 'rank', 'fill', 'business_kind')))
            # cache.set('poly', d, 60 * 60 * 24)
        resp = Response(d)
        resp["Access-Control-Allow-Origin"] = '*'
        resp["Access-Control-Allow-Methods"] = 'GET,PUT, OPTIONS'
        resp["Access-Control-Max-Age"] = '1000'
        resp["Access-Control-Allow-Headers"] = 'X-Requested-With, Content-Type'
        return resp


