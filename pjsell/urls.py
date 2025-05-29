from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_pjsell.urls')),  # ✅ CORRETO
    path('usuarios/', include('usuarios.urls')),
]


