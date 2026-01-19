from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('infrastructure.web_views.urls')), # Trỏ thẳng về web view
]