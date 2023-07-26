
from django.contrib import admin
from django.urls import path, include # new
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forecast.urls')), # new
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
