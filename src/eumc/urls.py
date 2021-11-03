from django.urls import path

from .views import *

app_name = 'eumc'

urlpatterns = [
    path('prn-count', PrnCountView.as_view(), name='prn-count'),
    path('prn-count/create', DrugInfoCreateView.as_view(), name='prn-count-create'),
]
