from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# Passo dois: Criar URLS de redirecionamento para cada aplicativo criado no projeto

urlpatterns = [
    path('admin/', admin.site.urls),
    # criar arquivo urls.py dentro da aplicação
    path('auth/', include('autenticacao.urls')),
    # criar arquivo urls.py dentro da aplicação
    path('', include('plataforma.urls')),
    
]
# criando url para arquivos de mídia 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
