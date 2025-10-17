from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from learning import views as learning_views  # import home_redirect view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # includes all account URLs
    path('', learning_views.home_redirect, name='home'),  # landing page / home
    path('', include('learning.urls')),  # include your learning app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
