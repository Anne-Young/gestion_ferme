from django.contrib.auth.backends import ModelBackend
from ferme.models import Utilisateur
 
 
class LoginBackend(ModelBackend):
    """
    Authentifie avec le champ 'login' + mot de passe.
    Le modèle a déjà USERNAME_FIELD = 'login', donc
    authenticate(username=...) fonctionne directement.
    """
 
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 'username' reçoit la valeur du champ USERNAME_FIELD (= 'login')
        login = username or kwargs.get('login')
        if not login or not password:
            return None
        try:
            user = Utilisateur.objects.get(login=login)
        except Utilisateur.DoesNotExist:
            return None
 
        if not user.check_password(password):
            return None
        if not user.actif:
            return None
        return user
 
    def get_user(self, user_id):
        try:
            return Utilisateur.objects.get(pk=user_id)
        except Utilisateur.DoesNotExist:
            return None