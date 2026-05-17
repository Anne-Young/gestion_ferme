
#  services/production_service.py


from django.core.exceptions import ValidationError
from django.db.models import Sum, Avg
from ferme.models import Production, Animal, Enclos


class ProductionService:

    @staticmethod
    def lister(type_produit=None, animal_id=None, enclos_id=None,
               date_debut=None, date_fin=None):
        qs = Production.objects.select_related('animal', 'enclos').order_by('-date_collecte')
        if type_produit:
            qs = qs.filter(type_produit=type_produit)
        if animal_id:
            qs = qs.filter(animal_id=animal_id)
        if enclos_id:
            qs = qs.filter(enclos_id=enclos_id)
        if date_debut:
            qs = qs.filter(date_collecte__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_collecte__lte=date_fin)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return Production.objects.select_related('animal', 'enclos').get(pk=pk)
        except Production.DoesNotExist:
            raise ValidationError(f"Production #{pk} introuvable.")

    @staticmethod
    def creer(data):
        animal_id = data.pop('animal_id', None) or data.pop('animal', None)
        enclos_id = data.pop('enclos_id', None) or data.pop('enclos', None)

        if not animal_id and not enclos_id:
            raise ValidationError("Un animal ou un enclos est requis.")

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

        prod = Production(**data)
        prod.full_clean()
        prod.save()
        return prod

    @staticmethod
    def modifier(pk, data):
        prod = ProductionService.obtenir(pk)
        if 'animal_id' in data or 'animal' in data:
            aid = data.pop('animal_id', None) or data.pop('animal', None)
            prod.animal = Animal.objects.get(pk=aid) if aid else None
        if 'enclos_id' in data or 'enclos' in data:
            eid = data.pop('enclos_id', None) or data.pop('enclos', None)
            prod.enclos = Enclos.objects.get(pk=eid) if eid else None
        for champ, valeur in data.items():
            setattr(prod, champ, valeur)
        prod.full_clean()
        prod.save()
        return prod

    @staticmethod
    def supprimer(pk):
        prod = ProductionService.obtenir(pk)
        prod.delete()
        return {'message': f"Production #{pk} supprimée."}

    @staticmethod
    def totaux_par_type(date_debut=None, date_fin=None):
        """Agrégation des quantités par type de produit."""
        qs = Production.objects.all()
        if date_debut:
            qs = qs.filter(date_collecte__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_collecte__lte=date_fin)
        return (qs.values('type_produit', 'unite')
                  .annotate(total=Sum('quantite'), moyenne=Avg('quantite'))
                  .order_by('type_produit'))
