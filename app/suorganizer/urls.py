"""suorganizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from catalog.urls import urlpatterns as catalogurls
from users.urls import user_urls as userurls
from users.urls import auth_urls as authurls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='catalog_index', permanent=False)),
    path('admin/', admin.site.urls),
    path('catalog/', include(catalogurls)),
    path('user/', include(userurls)),
    path('auth/', include(authurls))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
