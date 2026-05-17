
#  services/stock_aliment_service.py


from django.core.exceptions import ValidationError
from ferme.models import StockAliment, TypeAliment


class StockAlimentService:

    @staticmethod
    def lister(en_alerte_only=False):
        qs = StockAliment.objects.select_related('type_aliment').order_by('type_aliment__nom')
        if en_alerte_only:
            # Filtre Python car en_alerte est une property
            return [s for s in qs if s.en_alerte]
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return StockAliment.objects.select_related('type_aliment').get(pk=pk)
        except StockAliment.DoesNotExist:
            raise ValidationError(f"Stock aliment #{pk} introuvable.")

    @staticmethod
    def obtenir_par_aliment(type_aliment_id):
        try:
            return StockAliment.objects.select_related('type_aliment').get(
                type_aliment_id=type_aliment_id
            )
        except StockAliment.DoesNotExist:
            raise ValidationError(f"Aucun stock pour l'aliment #{type_aliment_id}.")

    @staticmethod
    def creer(data):
        ta_id = data.pop('type_aliment_id', None) or data.pop('type_aliment', None)
        if not ta_id:
            raise ValidationError("Le type d'aliment est obligatoire.")
        try:
            ta = TypeAliment.objects.get(pk=ta_id)
        except TypeAliment.DoesNotExist:
            raise ValidationError(f"Type d'aliment #{ta_id} introuvable.")
        if StockAliment.objects.filter(type_aliment=ta).exists():
            raise ValidationError(f"Un stock existe déjà pour '{ta.nom}'.")
        data['type_aliment'] = ta
        stock = StockAliment(**data)
        stock.full_clean()
        stock.save()
        return stock

    @staticmethod
    def modifier(pk, data):
        stock = StockAlimentService.obtenir(pk)
        data.pop('type_aliment_id', None)
        data.pop('type_aliment', None)
        for champ, valeur in data.items():
            setattr(stock, champ, valeur)
        stock.full_clean()
        stock.save()
        return stock

    @staticmethod
    def ajouter_stock(pk, quantite):
        """Ajoute une quantité au stock."""
        if quantite <= 0:
            raise ValidationError("La quantité doit être positive.")
        stock = StockAlimentService.obtenir(pk)
        stock.quantite_disponible += quantite
        stock.save(update_fields=['quantite_disponible', 'date_maj'])
        return stock

    @staticmethod
    def retirer_stock(pk, quantite):
        """Retire une quantité du stock (lors d'une distribution)."""
        if quantite <= 0:
            raise ValidationError("La quantité doit être positive.")
        stock = StockAlimentService.obtenir(pk)
        if stock.quantite_disponible < quantite:
            raise ValidationError(
                f"Stock insuffisant : {stock.quantite_disponible} disponible, {quantite} demandé."
            )
        stock.quantite_disponible -= quantite
        stock.save(update_fields=['quantite_disponible', 'date_maj'])
        return stock

    @staticmethod
    def supprimer(pk):
        stock = StockAlimentService.obtenir(pk)
        stock.delete()
        return {'message': "Stock supprimé."}
