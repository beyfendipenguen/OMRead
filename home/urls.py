from django.urls import path, include
from .views import omrView, homeView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homeView, name='home'),
    path('omr/', omrView, name='omr'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
