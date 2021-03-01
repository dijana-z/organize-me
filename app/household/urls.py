from django.urls import path, include
from rest_framework.routers import DefaultRouter

from household import views

router = DefaultRouter()
app_name = 'household'

router.register('household', views.HouseholdViewset)
router.register('grocery', views.GroceryViewSet)
router.register('grocerylist', views.GroceryListViewSet,
                basename='grocerylist')
router.register('shoppinglist', views.ShoppingListViewSet,
                basename='shoppinglist')

urlpatterns = [
    path('', include(router.urls))
]
