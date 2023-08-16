from django.urls import include, path
from django.contrib import admin

import theme.views

urlpatterns = [
    path('', theme.views.home),
    path('lote/', include('lote.urls')),
    path('relatorio/', include('relatorio.urls')),
    path('signup/', theme.views.signup_view, name='signup'),
    path('profile/', theme.views.profile, name='profile'),

    # Enable built-in authentication views
    path('accounts/', include('django.contrib.auth.urls')),    
    # Enable built-in admin interface
    path('admin/', admin.site.urls),
]
