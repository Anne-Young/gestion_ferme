
#  services/utilisateur_service.py


from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from ferme.models import Utilisateur


class UtilisateurService:

    #  LIST
    @staticmethod
    def lister(role=None, actif=None):
        """Retourne la liste des utilisateurs avec filtres optionnels."""
        qs = Utilisateur.objects.all().order_by('nom_complet')
        if role:
            qs = qs.filter(role=role)
        if actif is not None:
            qs = qs.filter(actif=actif)
        return qs

    #  GET
    @staticmethod
    def obtenir(pk):
        """Retourne un utilisateur ou lève une exception."""
        try:
            return Utilisateur.objects.get(pk=pk)
        except Utilisateur.DoesNotExist:
            raise ValidationError(f"Utilisateur #{pk} introuvable.")

    #  CREATE
    @staticmethod
    def creer(data):
        """
        Crée un nouvel utilisateur.
        data : dict avec nom_complet, login, password, role, telephone
        """
        login = data.get('login', '').strip()
        if Utilisateur.objects.filter(login=login).exists():
            raise ValidationError(f"Le login '{login}' est déjà utilisé.")

        password = data.pop('password', None)
        if not password:
            raise ValidationError("Le mot de passe est obligatoire.")

        utilisateur = Utilisateur(**data)
        utilisateur.set_password(password)
        utilisateur.full_clean()
        utilisateur.save()
        return utilisateur

    # UPDATE
    @staticmethod
    def modifier(pk, data):
        """Met à jour un utilisateur existant."""
        utilisateur = UtilisateurService.obtenir(pk)

        # Login unique (hors lui-même)
        new_login = data.get('login', utilisateur.login).strip()
        if (Utilisateur.objects.filter(login=new_login)
                               .exclude(pk=pk).exists()):
            raise ValidationError(f"Le login '{new_login}' est déjà utilisé.")

        # Gestion du mot de passe séparé
        password = data.pop('password', None)
        if password:
            utilisateur.set_password(password)

        for champ, valeur in data.items():
            setattr(utilisateur, champ, valeur)

        utilisateur.full_clean()
        utilisateur.save()
        return utilisateur

    #DELETE
    @staticmethod
    def supprimer(pk):
        """Désactive (soft-delete) un utilisateur plutôt que de le supprimer."""
        utilisateur = UtilisateurService.obtenir(pk)
        utilisateur.actif = False
        utilisateur.save(update_fields=['actif'])
        return {'message': f"Utilisateur '{utilisateur.nom_complet}' désactivé."}

    # AUTHENTICATE 
    @staticmethod
    def authentifier(login, password):
        """Authentifie un utilisateur et retourne l'objet si valide."""
        utilisateur = authenticate(username=login, password=password)
        if utilisateur is None:
            raise ValidationError("Login ou mot de passe incorrect.")
        if not utilisateur.actif:
            raise ValidationError("Ce compte est désactivé.")
        return utilisateur

    #  TOGGLE ACTIF
    @staticmethod
    def toggle_actif(pk):
        """Active ou désactive un utilisateur."""
        utilisateur = UtilisateurService.obtenir(pk)
        utilisateur.actif = not utilisateur.actif
        utilisateur.save(update_fields=['actif'])
        etat = "activé" if utilisateur.actif else "désactivé"
        return {'message': f"Utilisateur '{utilisateur.nom_complet}' {etat}.", 'actif': utilisateur.actif}
