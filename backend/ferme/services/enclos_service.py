
#  services/enclos_service.py


from django.core.exceptions import ValidationError
from ferme.models import Enclos


class EnclosService:

    @staticmethod
    def lister(type_enclos=None):
        qs = Enclos.objects.all().order_by('nom_enclos')
        if type_enclos:
            qs = qs.filter(type_enclos=type_enclos)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return Enclos.objects.get(pk=pk)
        except Enclos.DoesNotExist:
            raise ValidationError(f"Enclos #{pk} introuvable.")

    @staticmethod
    def creer(data):
        enclos = Enclos(**data)
        enclos.full_clean()
        enclos.save()
        return enclos

    @staticmethod
    def modifier(pk, data):
        enclos = EnclosService.obtenir(pk)
        for champ, valeur in data.items():
            setattr(enclos, champ, valeur)
        enclos.full_clean()
        enclos.save()
        return enclos

    @staticmethod
    def supprimer(pk):
        enclos = EnclosService.obtenir(pk)
        actifs = enclos.animaux.filter(statut='actif').count()
        if actifs > 0:
            raise ValidationError(
                f"Impossible de supprimer '{enclos.nom_enclos}' : {actifs} animal(aux) actif(s) présent(s)."
            )
        nom = enclos.nom_enclos
        enclos.delete()
        return {'message': f"Enclos '{nom}' supprimé."}

    @staticmethod
    def taux_occupation(pk):
        """Retourne le taux d'occupation d'un enclos."""
        enclos = EnclosService.obtenir(pk)
        return {
            'enclos': enclos.nom_enclos,
            'capacite_max': enclos.capacite_max,
            'nb_animaux_actifs': enclos.nb_animaux_actifs,
            'taux_occupation': enclos.taux_occupation,
        }
