from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/boards/', permanent=True)),
    path('admin/', admin.site.urls),
    path('hello/', include('hello.urls')),
    path('boards/', include('boards.urls')),
    path('accounts/', include('accounts.urls')),
]
