from re import template
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe


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
        obj = EumcDrugData.objects.first()
        rendered_table = create_prn(obj, **form.cleaned_data)
        context = {
            'table': mark_safe(rendered_table)
        }
        return render(request, 'eumc/prn_count_result.html', context)
