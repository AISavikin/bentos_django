from django import forms
from datetime import date
from .models import Employee  # Импорт модели Employee

class BaseRoadSheetForm(forms.Form):
    """Базовая форма для всех документов"""
    start_date = forms.DateField(
        label='Дата начала экспедиции',
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    days = forms.IntegerField(
        label='Количество дней',
        initial=5,
        min_value=1,
        widget=forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'})
    )
    destination = forms.ChoiceField(
        label='Место назначения',
        choices=[
            ('deneb', 'Денеб'),
            ('panov', 'Панов'),
            ('other', 'Другое')
        ],
        widget=forms.Select(attrs={'id': 'destination-select', 'class': 'form-select'})
    )
    other_destination = forms.CharField(
        label='Укажите место назначения',
        required=False,
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    add_weekend = forms.BooleanField(
        label='Заявление на работу в выходной',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class SingleRouteSheetForm(BaseRoadSheetForm):
    employee = forms.ModelChoiceField(
        label='Сотрудник',
        queryset=Employee.objects.all().order_by('name'),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'employee-select'})
    )
    objective = forms.CharField(
        label='Цель командировки',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class MultiRouteForm(BaseRoadSheetForm):
    employees = forms.ModelMultipleChoiceField(
        label='Сотрудники',
        queryset=Employee.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )


class BaseTbForm(forms.Form):
    start_date = forms.DateField(
        label='Дата начала экспедиции',
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    days = forms.IntegerField(
        label='Количество дней',
        initial=5,
        min_value=1
    )
    employees = forms.ModelMultipleChoiceField(
        label='Сотрудники',
        queryset=Employee.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )


class TbMixin:
    """Mixin с общими полями для TB-форм"""
    destination = forms.ChoiceField(
        label='Тип экспедиции',
        choices=[
            ('deneb', 'Денеб'),
            ('panov', 'Панов'),
            ('other', 'Береговая')
        ],
        widget=forms.Select(attrs={'id': 'destination-select'})
    )
    transport = forms.CharField(
        label='Транспорт',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Необязательно для морских экспедиций'
        })
    )
    driver = forms.CharField(
        label='Водитель',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Необязательно для морских экспедиций'
        })
    )
    phone_driver = forms.CharField(
        label='Номер телефона водителя',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Необязательно для морских экспедиций'
        })
    )
    exp_title = forms.CharField(
        label='Название экспедиции',
        max_length=255
    )


class ActForm(BaseTbForm, TbMixin):
    exp_leader = forms.ModelChoiceField(
        label='Начальник экспедиции',
        queryset=Employee.objects.all().order_by('name'),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class ProtocolForm(BaseTbForm):
    exp_title = forms.CharField(
        label='Название экспедиции',
        max_length=255
    )


class RaspiskaForm(BaseTbForm):
    exp_title = forms.CharField(
        label='Название экспедиции',
        max_length=255
    )


class InfoListForm(BaseTbForm, TbMixin):
    exp_leader = forms.ModelChoiceField(
        label='Начальник экспедиции',
        queryset=Employee.objects.all().order_by('name'),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    exp_sim = forms.CharField(
        label='Номер экспедиционной сим-карты',
        max_length=255
    )
    work_region = forms.CharField(
        label='Район исследований',
        max_length=255
    )


class AllTbForm(InfoListForm, TbMixin):
    pass