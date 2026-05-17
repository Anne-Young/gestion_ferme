
#  services/vente_service.py


from django.core.exceptions import ValidationError
from django.db.models import Sum
from ferme.models import Vente
from .stock_produit_service import StockProduitService


class VenteService:

    @staticmethod
    def lister(type_produit=None, date_debut=None, date_fin=None, acheteur=None):
        qs = Vente.objects.all().order_by('-date_vente')
        if type_produit:
            qs = qs.filter(type_produit=type_produit)
        if date_debut:
            qs = qs.filter(date_vente__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_vente__lte=date_fin)
        if acheteur:
            qs = qs.filter(acheteur__icontains=acheteur)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return Vente.objects.get(pk=pk)
        except Vente.DoesNotExist:
            raise ValidationError(f"Vente #{pk} introuvable.")

    @staticmethod
    def creer(data, deduire_stock=True):
        """
        Enregistre une vente.
        Si deduire_stock=True et type_produit != 'animal_vivant',
        soustrait du stock produit correspondant.
        """
        vente = Vente(**data)
        vente.full_clean()

        if deduire_stock and data.get('type_produit') != 'animal_vivant':
            # Mappage vente → stock produit
            mapping = {
                'lait':    'lait',
                'viande':  'viande',
                'oeuf':    'oeuf',
                'engrais': 'engrais_traite',
            }
            tp_stock = mapping.get(data.get('type_produit'))
            if tp_stock:
                StockProduitService.retirer_stock(tp_stock, float(data['quantite_vendue']))

        vente.save()
        return vente

    @staticmethod
    def modifier(pk, data):
        vente = VenteService.obtenir(pk)
        for champ, valeur in data.items():
            setattr(vente, champ, valeur)
        vente.full_clean()
        vente.save()
        return vente

    @staticmethod
    def supprimer(pk):
        vente = VenteService.obtenir(pk)
        vente.delete()
        return {'message': f"Vente #{pk} supprimée."}

    @staticmethod
    def chiffre_affaires(date_debut=None, date_fin=None):
        """Calcule le CA total sur une période."""
        from django.db.models import ExpressionWrapper, F, DecimalField
        qs = Vente.objects.all()
        if date_debut:
            qs = qs.filter(date_vente__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_vente__lte=date_fin)
        total = sum(v.montant_total for v in qs)
        par_type = (qs.values('type_produit')
                      .annotate(total_qte=Sum('quantite_vendue'))
                      .order_by('-total_qte'))
        return {'total_mga': total, 'par_type': list(par_type)}
