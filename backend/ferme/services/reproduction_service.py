
#  services/reproduction_service.py


from django.core.exceptions import ValidationError
from ferme.models import Reproduction, Animal


class ReproductionService:

    @staticmethod
    def lister(mere_id=None, pere_id=None, date_debut=None, date_fin=None):
        qs = (Reproduction.objects
              .select_related('mere', 'pere')
              .order_by('-date_naissance'))
        if mere_id:
            qs = qs.filter(mere_id=mere_id)
        if pere_id:
            qs = qs.filter(pere_id=pere_id)
        if date_debut:
            qs = qs.filter(date_naissance__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_naissance__lte=date_fin)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return Reproduction.objects.select_related('mere', 'pere').get(pk=pk)
        except Reproduction.DoesNotExist:
            raise ValidationError(f"Reproduction #{pk} introuvable.")

    @staticmethod
    def creer(data):
        mere_id = data.pop('mere_id', None) or data.pop('mere', None)
        pere_id = data.pop('pere_id', None) or data.pop('pere', None)

        if mere_id:
            try:
                mere = Animal.objects.get(pk=mere_id)
                if mere.sexe != 'F':
                    raise ValidationError(f"L'animal #{mere_id} n'est pas une femelle.")
                data['mere'] = mere
            except Animal.DoesNotExist:
                raise ValidationError(f"Animal mère #{mere_id} introuvable.")

        if pere_id:
            try:
                pere = Animal.objects.get(pk=pere_id)
                if pere.sexe != 'M':
                    raise ValidationError(f"L'animal #{pere_id} n'est pas un mâle.")
                data['pere'] = pere
            except Animal.DoesNotExist:
                raise ValidationError(f"Animal père #{pere_id} introuvable.")

        # Cohérence survivants ≤ naissances
        nb = data.get('nb_naissances')
        surv = data.get('nb_survivants')
        if nb and surv and surv > nb:
            raise ValidationError("Les survivants ne peuvent pas dépasser les naissances.")

        repro = Reproduction(**data)
        repro.full_clean()
        repro.save()
        return repro

    @staticmethod
    def modifier(pk, data):
        repro = ReproductionService.obtenir(pk)
        if 'mere_id' in data or 'mere' in data:
            mid = data.pop('mere_id', None) or data.pop('mere', None)
            repro.mere = Animal.objects.get(pk=mid) if mid else None
        if 'pere_id' in data or 'pere' in data:
            pid = data.pop('pere_id', None) or data.pop('pere', None)
            repro.pere = Animal.objects.get(pk=pid) if pid else None
        for champ, valeur in data.items():
            setattr(repro, champ, valeur)
        repro.full_clean()
        repro.save()
        return repro

    @staticmethod
    def supprimer(pk):
        repro = ReproductionService.obtenir(pk)
        repro.delete()
        return {'message': f"Reproduction #{pk} supprimée."}

    @staticmethod
    def taux_survie_global():
        """Calcule le taux de survie moyen sur toutes les portées."""
        repros = Reproduction.objects.exclude(
            nb_naissances=None
        ).exclude(nb_survivants=None).exclude(nb_naissances=0)
        if not repros:
            return {'taux_survie_moyen': None}
        total = sum(r.nb_survivants / r.nb_naissances * 100 for r in repros)
        return {'taux_survie_moyen': round(total / repros.count(), 1), 'nb_portees': repros.count()}
