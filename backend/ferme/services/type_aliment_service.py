
#  services/type_aliment_service.py


from django.core.exceptions import ValidationError
from ferme.models import TypeAliment


class TypeAlimentService:

    @staticmethod
    def lister(categorie=None, origine=None):
        qs = TypeAliment.objects.all().order_by('nom')
        if categorie:
            qs = qs.filter(categorie=categorie)
        if origine:
            qs = qs.filter(origine=origine)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return TypeAliment.objects.get(pk=pk)
        except TypeAliment.DoesNotExist:
            raise ValidationError(f"Type d'aliment #{pk} introuvable.")

    @staticmethod
    def creer(data):
        nom = data.get('nom', '').strip()
        if TypeAliment.objects.filter(nom__iexact=nom).exists():
            raise ValidationError(f"L'aliment '{nom}' existe déjà.")
        aliment = TypeAliment(**data)
        aliment.full_clean()
        aliment.save()
        return aliment

    @staticmethod
    def modifier(pk, data):
        aliment = TypeAlimentService.obtenir(pk)
        nom = data.get('nom', aliment.nom).strip()
        if TypeAliment.objects.filter(nom__iexact=nom).exclude(pk=pk).exists():
            raise ValidationError(f"L'aliment '{nom}' existe déjà.")
        for champ, valeur in data.items():
            setattr(aliment, champ, valeur)
        aliment.full_clean()
        aliment.save()
        return aliment

    @staticmethod
    def supprimer(pk):
        aliment = TypeAlimentService.obtenir(pk)
        if aliment.distributions.exists():
            raise ValidationError(
                f"Impossible de supprimer '{aliment.nom}' : des distributions y sont liées."
            )
        nom = aliment.nom
        aliment.delete()
        return {'message': f"Aliment '{nom}' supprimé."}
