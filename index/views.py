from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ['https://i.ibb.co/nMwsgw7W/main-page-5.jpg',
                           'https://i.ibb.co/0yFttQ3T/main-page-2.jpg',
                           'https://i.ibb.co/wZTLfLm9/main-page-3.jpg',]
        return context

class InDevelopmentView(TemplateView):
    template_name = 'in_development.html'