
#  services/stock_produit_service.py


from django.core.exceptions import ValidationError
from ferme.models import StockProduit


class StockProduitService:

    @staticmethod
    def lister(en_alerte_only=False):
        qs = StockProduit.objects.all().order_by('type_produit')
        if en_alerte_only:
            return [s for s in qs if s.en_alerte]
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return StockProduit.objects.get(pk=pk)
        except StockProduit.DoesNotExist:
            raise ValidationError(f"Stock produit #{pk} introuvable.")

    @staticmethod
    def obtenir_par_type(type_produit):
        try:
            return StockProduit.objects.get(type_produit=type_produit)
        except StockProduit.DoesNotExist:
            raise ValidationError(f"Aucun stock pour le type '{type_produit}'.")

    @staticmethod
    def creer(data):
        tp = data.get('type_produit')
        if StockProduit.objects.filter(type_produit=tp).exists():
            raise ValidationError(f"Un stock existe déjà pour '{tp}'.")
        stock = StockProduit(**data)
        stock.full_clean()
        stock.save()
        return stock

    @staticmethod
    def modifier(pk, data):
        stock = StockProduitService.obtenir(pk)
        for champ, valeur in data.items():
            setattr(stock, champ, valeur)
        stock.full_clean()
        stock.save()
        return stock

    @staticmethod
    def ajouter_stock(type_produit, quantite):
        """Appelé après chaque collecte de production."""
        if quantite <= 0:
            raise ValidationError("La quantité doit être positive.")
        stock = StockProduitService.obtenir_par_type(type_produit)
        stock.quantite_disponible += quantite
        stock.save(update_fields=['quantite_disponible', 'date_maj'])
        return stock

    @staticmethod
    def retirer_stock(type_produit, quantite):
        """Appelé lors d'une vente."""
        if quantite <= 0:
            raise ValidationError("La quantité doit être positive.")
        stock = StockProduitService.obtenir_par_type(type_produit)
        if stock.quantite_disponible < quantite:
            raise ValidationError(
                f"Stock insuffisant : {stock.quantite_disponible} {stock.unite} disponible."
            )
        stock.quantite_disponible -= quantite
        stock.save(update_fields=['quantite_disponible', 'date_maj'])
        return stock

    @staticmethod
    def supprimer(pk):
        stock = StockProduitService.obtenir(pk)
        stock.delete()
        return {'message': "Stock produit supprimé."}
