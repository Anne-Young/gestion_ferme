#  services/espece_service.py


from django.core.exceptions import ValidationError
from ferme.models import Espece


class EspeceService:

    @staticmethod
    def lister():
        return Espece.objects.all().order_by('nom_espece')

    @staticmethod
    def obtenir(pk):
        try:
            return Espece.objects.get(pk=pk)
        except Espece.DoesNotExist:
            raise ValidationError(f"Espèce #{pk} introuvable.")

    @staticmethod
    def creer(data):
        nom = data.get('nom_espece', '').strip()
        if Espece.objects.filter(nom_espece__iexact=nom).exists():
            raise ValidationError(f"L'espèce '{nom}' existe déjà.")
        espece = Espece(**data)
        espece.full_clean()
        espece.save()
        return espece

    @staticmethod
    def modifier(pk, data):
        espece = EspeceService.obtenir(pk)
        nom = data.get('nom_espece', espece.nom_espece).strip()
        if Espece.objects.filter(nom_espece__iexact=nom).exclude(pk=pk).exists():
            raise ValidationError(f"L'espèce '{nom}' existe déjà.")
        for champ, valeur in data.items():
            setattr(espece, champ, valeur)
        espece.full_clean()
        espece.save()
        return espece

    @staticmethod
    def supprimer(pk):
        espece = EspeceService.obtenir(pk)
        if espece.races.exists():
            raise ValidationError(
                f"Impossible de supprimer '{espece.nom_espece}' : des races y sont rattachées."
            )
        nom = espece.nom_espece
        espece.delete()
        return {'message': f"Espèce '{nom}' supprimée."}
