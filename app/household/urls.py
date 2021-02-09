from django.urls import path, include
from rest_framework.routers import DefaultRouter

from household import views

router = DefaultRouter()

router.register('users', views.BaseHouseholdViewset)

app_name = 'household'

urlpatterns = [
    path('', include(router.urls))
]
