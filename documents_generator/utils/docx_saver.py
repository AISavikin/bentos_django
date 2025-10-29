from datetime import timedelta, datetime
from io import BytesIO
from docxtpl import DocxTemplate
from typing import Dict
from app.documents.config import *
from .holydays_updater import get_weekends, load_holidays_from_json, is_work_day

# Импорт модулей данных


class DocumentGenerator:
    """Класс для генерации документов Word на основе шаблонов"""

    def __init__(self):
        self.path_to_templates = Path(__file__).parent.joinpath('docx_templates')

    def _calculate_dates(self, start_date: datetime, days: int) -> Dict:
        """Рассчитывает даты для документа"""
        end_date = start_date + timedelta(days=days - 1)
        return {
            'start_day': start_date.day,
            'start_month': MONTH_GENITIVE[start_date.month],
            'start_year': start_date.strftime('%y'),
            'end_day': end_date.day,
            'end_month': MONTH_GENITIVE[end_date.month],
            'end_year': end_date.strftime('%y')
        }

    def _process_employees(self, employees: list, objective: str) -> None:
        """Назначает цель сотрудникам"""
        if objective:
            for emp in employees:
                emp.objective = objective


    def _get_string_dates(self, start_date: datetime, days: int) -> str:
        calculated_dates = self._calculate_dates(start_date, days)
        if calculated_dates['start_month'] == calculated_dates['end_month']:
            dates = f'С {calculated_dates["start_day"]} по {calculated_dates["end_day"]} {calculated_dates["start_month"]} {start_date.year} года'
        else:
            dates = f'С {calculated_dates["start_day"]} {calculated_dates["start_month"]} по {calculated_dates["end_day"]} {calculated_dates["end_month"]} {start_date.year} года'
        return dates

    def _get_sign_date(self, start_date: datetime) -> str:
        holidays = load_holidays_from_json()
        sign_date = start_date - timedelta(days=1)
        while not is_work_day(sign_date, holidays):
            sign_date = sign_date - timedelta(days=1)
        return f'{sign_date.day}.{sign_date.month:02d}.{sign_date.year}'

    def prepare_tb_context(self, context: Dict) -> Dict:
        validated_context = context.copy()
        validated_context['dates'] = self._get_string_dates(validated_context['start_date'],
                                                            validated_context['days']
                                                            )

        validated_context['sign_date'] = self._get_sign_date(validated_context['start_date'])

        return validated_context

    def prepare_road_sheet_context(self, context: Dict) -> Dict:
        """Подготавливает контекст для шаблона"""
        validated_context = context.copy()
        # Обработка дат
        date_ctx = self._calculate_dates(
            validated_context['start_date'],
            validated_context['days']
        )
        validated_context.update(date_ctx)

        # Обработка сотрудников
        self._process_employees(
            validated_context['employees'],
            validated_context.get('objective', '')
        )

        # Форматирование выходных дней
        weekends = get_weekends(
            validated_context['start_date'],
            validated_context['days']
        )
        validated_context['weekends'] = ', '.join(
            f'{day.day}.{day.month:02d}' for day in weekends
        )
        # Форматирование даты документа
        validated_context['sign_date'] = self._get_sign_date(validated_context['start_date'])
        return validated_context

    def generate_document(self, context: Dict) -> BytesIO:
        """Генерирует документ Word"""
        template_name = context['template']
        prepared_context = {}
        if template_name == 'road_sheet_tpl':
            prepared_context.update(self.prepare_road_sheet_context(context))
        elif template_name == 'tb_tpl':
            prepared_context.update(self.prepare_tb_context(context))

        else:
            raise Exception('Не указан шаблон')

        memory_file = BytesIO()
        template = DocxTemplate(self.path_to_templates / f'{template_name}.docx')
        template.render(prepared_context)
        template.save(memory_file)
        memory_file.seek(0)

        return memory_file




