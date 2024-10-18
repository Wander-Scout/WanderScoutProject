
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  
    path('restaurant/', include('restaurant.urls')),
    path('image_display/', include('image_display.urls')),

]