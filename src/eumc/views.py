from re import template
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy

from .models import EumcDrugData
from .forms import PrnDataInputForm
from .services import create_prn


def prn_count(request):
    form = PrnDataInputForm(request.POST or None)
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, 'eumc/prn_count.html', context)
    if form.is_valid():
        prn_data = form.cleaned_data['data']
        inj_groups = form.cleaned_data['injgroups']
        obj = EumcDrugData.objects.last()
        ret = create_prn(obj, prn_data, inj_groups)
        context = {
            'prn_list': ret.to_dict('record')
        }
        return render(request, 'eumc/prn_count_result.html', context)
