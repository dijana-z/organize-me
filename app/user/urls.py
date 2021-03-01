from django.urls import path

from . import views


app_name = 'user'

urlpatterns = [
    # TODO: get vraca 405?
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserViews.as_view(), name='me'),
]
