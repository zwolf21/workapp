import logging

from django.shortcuts import render

from django.utils.safestring import mark_safe
from django.views.generic import FormView
from hitcount.views import HitCountDetailView

from .models import EumcDrugData
from .forms import PrnDataInputForm
from .services import create_prn


logger = logging.getLogger('eumc')

class PrnCountView(FormView, HitCountDetailView):
    model = EumcDrugData
    template_name = 'eumc/prn_count.html'
    form_class = PrnDataInputForm
    success_url = '.'
    count_hit = True

    def get_object(self, queryset=None):
        self.object = EumcDrugData.objects.first()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PrnDataInputForm(None)
        context['form'] = form
        return context
    
    def form_valid(self, form):
        super().form_valid(form)
        object = self.get_object()

        rendered_table = create_prn(object, **form.cleaned_data)
        
        logger.info({
            'injgroups': form.cleaned_data['injgroups'],
            'bywords': form.cleaned_data['bywords']
        })

        context = {
            'table': mark_safe(rendered_table)
        }
        return render(self.request, 'eumc/prn_count_result.html', context)
