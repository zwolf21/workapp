import logging
from django.forms import fields

from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.generic import FormView, CreateView
from hitcount.views import HitCountDetailView

from .models import EumcDrugData
from .forms import PrnDataInputForm, DrugUpdateForm
from .services import create_prn


logger = logging.getLogger('eumc')



class PrnCountView(FormView, HitCountDetailView):
    model = EumcDrugData
    template_name = 'eumc/prn_count.html'
    form_class = PrnDataInputForm
    success_url = '.'
    count_hit = True

    def get_object(self, queryset=None):
        self.object = EumcDrugData.objects.latest()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PrnDataInputForm(None)
        context['form'] = form
        return context
    
    def form_valid(self, form):
        super().form_valid(form)
        object = self.get_object()

        rendered_table, not_exists_in_druginfo = create_prn(object, **form.cleaned_data)

        if not_exists_in_druginfo:
            count = len(not_exists_in_druginfo)
            drug, *_ = not_exists_in_druginfo 
            msg = f'''{drug} 등 {count} 건의 항목이 약품정보에 등록되어 있지 않아 집계되지 않았습니다. 약품정보를 업데이트 해야합니다.
                (신약이 추가된 경우 약품정보를 업데이트 하지 않으면 집계 되지 않을 수 있음)
            '''
            messages.add_message(self.request, messages.WARNING, msg)
            logger.info({'not_counted': not_exists_in_druginfo})
        
        logger.info({
            'injgroups': form.cleaned_data['injgroups'],
            'bywords': form.cleaned_data['bywords']
        })

        context = {
            'table': mark_safe(rendered_table)
        }
        return render(self.request, 'eumc/prn_count_result.html', context)



class DrugInfoCreateView(CreateView):
    model = EumcDrugData
    form_class = DrugUpdateForm
    success_url = reverse_lazy('eumc:prn-count')
    template_name = 'eumc/druginfo_create.html'



