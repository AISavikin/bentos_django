from django.urls import path
from . import views

app_name = 'documents_generator'

urlpatterns = [
    path('', views.DocumentsIndexView.as_view(), name='documents_index'),
    path('single-route/', views.SingleRouteSheetView.as_view(), name='single_route'),
    path('multi-route/', views.MultiRouteFormView.as_view(), name='multi_route'),
    path('act/', views.ActFormView.as_view(), name='act'),
    path('protocol/', views.ProtocolFormView.as_view(), name='protocol'),
    path('raspiska/', views.RaspiskaFormView.as_view(), name='raspiska'),
    path('info-list/', views.InfoListView.as_view(), name='info_list'),
    path('all-tb/', views.AllTbFormView.as_view(), name='all_tb'),
    path('get-employee-data/<int:employee_id>/', views.GetEmployeeDataView.as_view(), name='get_employee_data'),
]