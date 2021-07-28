from django.urls import path

from .views import prn_count

app_name = 'eumc'

urlpatterns = [
    path('prn-count', prn_count, name='prn-count')
]