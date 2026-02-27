from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_reports, name='reports_dashboard'),
    path('profit-loss/', views.profit_loss_report, name='profit_loss_report'),
    path('sales/', views.sales_report, name='sales_report'),
    path('labour/', views.labour_report, name='labour_report'),
]
