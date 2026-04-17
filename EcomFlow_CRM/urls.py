
from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # ربط التطبيقات (Apps)
    path('clients/', include('apps.clients.urls')),
    path('products/', include('apps.products.urls')),
    path('automations/', include('apps.automations.urls')),
    path('ventes/', include('apps.ventes.urls')),
    path('',include('apps.accounts.urls')),
    

]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
