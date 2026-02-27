from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# NEW: Import dashboard view
from apps.billing.views import dashboard  # ← Add this line

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # Dashboard at root URL
    path('', dashboard, name='dashboard'),  # ← Added this line
    
    # Apps
    path('', include('apps.core.urls')),  # If core has other paths, keep this
    path('products/', include('apps.products.urls')),
    path('billing/', include('apps.billing.urls')),
    path('customers/', include('apps.customers.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('labour/', include('apps.labour.urls')),
    path('reports/', include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)