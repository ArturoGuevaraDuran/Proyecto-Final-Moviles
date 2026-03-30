from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aquí le decimos a Django: "Todo lo que empiece con api/, búscalo en api.urls"
    path('api/', include('api.urls')),
]