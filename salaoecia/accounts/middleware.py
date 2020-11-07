import time
from datetime import datetime

from django.contrib.auth import logout
from django.http import HttpResponseRedirect

class SessionExpiredMiddleware:
    def __init__(self, get_response):
        """
        :Nome da classe/função: __init__
        :descrição: Define a resposta ao inicializar a classe
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :param get_response: Resposta
        """
        self.get_response = get_response

    def __call__(self, request):
        try:
            now = time.time()
            if 'last_activity' not in request.session:
                request.session['last_activity'] = time.time()
            last_activity = request.session['last_activity']
            ultima_atividade = datetime.fromtimestamp(last_activity)
            agora = datetime.now()
            if (agora - ultima_atividade).min > 10:
                logout(request)
                return HttpResponseRedirect("login")

            if not request.is_ajax():
                request.session['last_activity'] = time.time()
        except:
            pass
        return self.get_response(request)