from django.contrib.auth.backends import BaseBackend

from salaoecia.accounts.models import User


class QuantidadeLoginView(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user = User.objects.all().filter(username=username).first()
        if user is not None and not user.check_password(raw_password=password):
            if user.tentativas_login is None:
                user.tentativas_login = 1
            else:
                user.tentativas_login += 1

            if user.tentativas_login >= 3:
                user.is_active = False
        else:
            user.tentativas_login = 0
        user.save()