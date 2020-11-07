"""salaoecia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from .core import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .accounts import views as viewsaccounts
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [

    path('admin/', admin.site.urls),
    # path('home/', viewsberas.index),
    #url(r'^$', viewsberas.index, name='home'),
    path('entrar/', LoginView.as_view(template_name='accounts/login_bs.html'), name='login'),
    path('cadastre-se/', viewsaccounts.register, name='register'),
    path('desativar/', login_required(viewsaccounts.DesativarContaView.as_view()), name='desativar'),
    path('nova-senha/', viewsaccounts.password_reset, name='password_reset'),
    path('confirmar-nova-senha/<key>/', viewsaccounts.password_reset_confirm, name='password_reset_confirm'),
    path('editar/', viewsaccounts.edit, name='edit'),
    path('alterar-senha/', viewsaccounts.edit_password, name='edit_password'),
    path('conta/', viewsaccounts.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page=views.home), name='logout'),
    path('sair/', LogoutView.as_view(next_page='salao.agendamento'), name='logout'),
    path('', include('salaoecia.salao.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
