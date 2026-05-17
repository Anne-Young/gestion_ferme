
#  services/alimentation_service.py


from django.core.exceptions import ValidationError
from ferme.models import AlimentationAnimal, Animal, Enclos, TypeAliment
from .stock_aliment_service import StockAlimentService


class AlimentationService:

    @staticmethod
    def lister(animal_id=None, enclos_id=None, type_aliment_id=None,
               date_debut=None, date_fin=None):
        qs = (AlimentationAnimal.objects
              .select_related('animal', 'enclos', 'type_aliment')
              .order_by('-date_distribution'))
        if animal_id:
            qs = qs.filter(animal_id=animal_id)
        if enclos_id:
            qs = qs.filter(enclos_id=enclos_id)
        if type_aliment_id:
            qs = qs.filter(type_aliment_id=type_aliment_id)
        if date_debut:
            qs = qs.filter(date_distribution__date__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_distribution__date__lte=date_fin)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return AlimentationAnimal.objects.select_related(
                'animal', 'enclos', 'type_aliment'
            ).get(pk=pk)
        except AlimentationAnimal.DoesNotExist:
            raise ValidationError(f"Distribution #{pk} introuvable.")

    @staticmethod
    def creer(data, deduire_stock=True):
        """
        Enregistre une distribution alimentaire.
        Déduit automatiquement du stock si deduire_stock=True.
        """
        animal_id = data.pop('animal_id', None) or data.pop('animal', None)
        enclos_id = data.pop('enclos_id', None) or data.pop('enclos', None)
        ta_id     = data.pop('type_aliment_id', None) or data.pop('type_aliment', None)

        if not animal_id and not enclos_id:
            raise ValidationError("Un animal ou un enclos est requis.")
        if not ta_id:
            raise ValidationError("Le type d'aliment est obligatoire.")

        try:
            data['type_aliment'] = TypeAliment.objects.get(pk=ta_id)
        except TypeAliment.DoesNotExist:
            raise ValidationError(f"Aliment #{ta_id} introuvable.")

        if animal_id:
            try:
                data['animal'] = Animal.objects.get(pk=animal_id)
            except Animal.DoesNotExist:
                raise ValidationError(f"Animal #{animal_id} introuvable.")
        if enclos_id:
            try:
                data['enclos'] = Enclos.objects.get(pk=enclos_id)
            except Enclos.DoesNotExist:
                raise ValidationError(f"Enclos #{enclos_id} introuvable.")

        distribution = AlimentationAnimal(**data)
        distribution.full_clean()

        # Déduction du stock
        if deduire_stock:
            stock = data['type_aliment'].stock
            StockAlimentService.retirer_stock(stock.pk, float(data['quantite']))

        distribution.save()
        return distribution

    @staticmethod
    def modifier(pk, data):
        dist = AlimentationService.obtenir(pk)
        data.pop('animal_id', None)
        data.pop('animal', None)
        data.pop('enclos_id', None)
        data.pop('enclos', None)
        data.pop('type_aliment_id', None)
        data.pop('type_aliment', None)
        for champ, valeur in data.items():
            setattr(dist, champ, valeur)
        dist.full_clean()
        dist.save()
        return dist

    @staticmethod
    def supprimer(pk):
        dist = AlimentationService.obtenir(pk)
        dist.delete()
        return {'message': f"Distribution #{pk} supprimée."}
