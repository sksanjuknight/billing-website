from django.urls import path
from . import views

urlpatterns = [
    # Labour management
    path('', views.labour_list, name='labour_list'),
    path('create/', views.labour_create, name='labour_create'),
    path('<int:pk>/', views.labour_detail, name='labour_detail'),
    path('<int:pk>/edit/', views.labour_edit, name='labour_edit'),
    path('<int:pk>/delete/', views.labour_delete, name='labour_delete'),
    path('<int:pk>/attendance/', views.mark_attendance, name='mark_attendance'),
    
    # Wage management
    path('wages/', views.wage_summary, name='wage_summary'),
    path('wages/record/', views.record_wage_payment, name='record_wage_payment'),
]
