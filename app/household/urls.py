from django.urls import path, include
from rest_framework.routers import DefaultRouter

from household import views

router = DefaultRouter()
app_name = 'household'

router.register('household', views.HouseholdViewset)


urlpatterns = [
    path('', include(router.urls))
]
