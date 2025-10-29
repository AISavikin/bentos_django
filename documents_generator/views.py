from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Employee
from .forms import (
    SingleRouteSheetForm, MultiRouteForm, ActForm,
    ProtocolForm, RaspiskaForm, InfoListForm, AllTbForm
)


class DocumentsIndexView(TemplateView):
    template_name = 'documents_generator/documents_index.html'


class BaseDocumentFormView(FormView):
    """Базовый класс для всех форм документов"""
    success_url = reverse_lazy('documents_index')  # или ваш URL успеха

    def form_valid(self, form):
        # Здесь можно обработать данные формы после валидации
        # form.cleaned_data содержит проверенные данные
        print("Форма валидна!", form.cleaned_data)
        return super().form_valid(form)


class SingleRouteSheetView(BaseDocumentFormView):
    template_name = 'documents_generator/route_sheet.html'
    form_class = SingleRouteSheetForm
    # success_url = reverse_lazy('success_page')  # можно переопределить


class MultiRouteFormView(BaseDocumentFormView):
    template_name = 'documents_generator/route_sheet.html'
    form_class = MultiRouteForm


class ActFormView(BaseDocumentFormView):
    form_class = ActForm


class ProtocolFormView(BaseDocumentFormView):
    form_class = ProtocolForm


class RaspiskaFormView(BaseDocumentFormView):
    form_class = RaspiskaForm


class InfoListView(BaseDocumentFormView):
    form_class = InfoListForm


class AllTbFormView(BaseDocumentFormView):
    form_class = AllTbForm


class GetEmployeeDataView(TemplateView):
    """View для AJAX запроса данных сотрудника"""

    def get(self, request, *args, **kwargs):
        employee_id = self.kwargs.get('employee_id')
        employee = get_object_or_404(Employee, id=employee_id)

        return JsonResponse({
            'objective': employee.objective,
            'name': employee.name,
            'position': str(employee.position),
            'department': str(employee.department),
            'profession': employee.profession,
        })