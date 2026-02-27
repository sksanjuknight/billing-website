from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('create/', views.invoice_create, name='invoice_create'),

    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),

    # NEW
    path('<int:pk>/add-payment/', views.invoice_add_payment, name='invoice_add_payment'),
    path('<int:pk>/mark-paid/', views.invoice_mark_paid, name='invoice_mark_paid'),

    path('<int:pk>/status/', views.invoice_update_status, name='invoice_update_status'),
    path('<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
]
