from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from foodgram_project.settings import STATIC_ROOT, STATIC_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(STATIC_URL, document_root=STATIC_ROOT)
