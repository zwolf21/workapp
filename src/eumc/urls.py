from django.urls import path

from .views import  PrnCountView

app_name = 'eumc'

urlpatterns = [
    path('prn-count', PrnCountView.as_view(), name='prn-count'),
]
