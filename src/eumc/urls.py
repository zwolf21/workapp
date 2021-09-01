from django.urls import path

from .views import  PrnCountView

app_name = 'eumc'

urlpatterns = [
    # path('prn-count', prn_count, name='prn-count'),
    path('prn-count-test', PrnCountView.as_view(), name='prn-count-test'),
]