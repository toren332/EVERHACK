from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken import views as rf_views
from . import views

app_name = 'EVERHACK'
router = routers.DefaultRouter()

router.register('building', views.BuildingViewSet, basename='building')
router.register('poly', views.PolyViewSet, basename='poly')

urlpatterns = router.urls

urlpatterns += [
    # path('verify/check_email_code/', views.VerifyCheckEmailCode.as_view(), name='verify_email'),
]
