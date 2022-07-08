from django.contrib import admin
from django.urls import path, include


# Passo dois: Criar URLS de redirecionamento para cada aplicativo criado no projeto

urlpatterns = [
    path('admin/', admin.site.urls),
    # criar arquivo urls.py dentro da aplicação
    path('auth/', include('autenticacao.urls')),
    # criar arquivo urls.py dentro da aplicação
    path('', include('plataforma.urls')),
    
]
