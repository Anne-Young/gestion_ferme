
#  services/engrais_service.py


from django.core.exceptions import ValidationError
from ferme.models import Engrais, Enclos


class EngraisService:

    @staticmethod
    def lister(statut=None, type_engrais=None, enclos_id=None):
        qs = Engrais.objects.select_related('enclos').order_by('-date_collecte')
        if statut:
            qs = qs.filter(statut_traitement=statut)
        if type_engrais:
            qs = qs.filter(type_engrais=type_engrais)
        if enclos_id:
            qs = qs.filter(enclos_id=enclos_id)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return Engrais.objects.select_related('enclos').get(pk=pk)
        except Engrais.DoesNotExist:
            raise ValidationError(f"Engrais #{pk} introuvable.")

    @staticmethod
    def creer(data):
        enclos_id = data.pop('enclos_id', None) or data.pop('enclos', None)
        if enclos_id:
            try:
                data['enclos'] = Enclos.objects.get(pk=enclos_id)
            except Enclos.DoesNotExist:
                raise ValidationError(f"Enclos #{enclos_id} introuvable.")
        engrais = Engrais(**data)
        engrais.full_clean()
        engrais.save()
        return engrais

    @staticmethod
    def modifier(pk, data):
        engrais = EngraisService.obtenir(pk)
        if 'enclos_id' in data or 'enclos' in data:
            eid = data.pop('enclos_id', None) or data.pop('enclos', None)
            engrais.enclos = Enclos.objects.get(pk=eid) if eid else None
        for champ, valeur in data.items():
            setattr(engrais, champ, valeur)
        engrais.full_clean()
        engrais.save()
        return engrais

    @staticmethod
    def changer_statut(pk, nouveau_statut):
        valides = [s[0] for s in Engrais.STATUT_CHOICES]
        if nouveau_statut not in valides:
            raise ValidationError(f"Statut invalide. Choix : {valides}")
        engrais = EngraisService.obtenir(pk)
        engrais.statut_traitement = nouveau_statut
        engrais.save(update_fields=['statut_traitement'])
        return engrais

    @staticmethod
    def supprimer(pk):
        engrais = EngraisService.obtenir(pk)
        engrais.delete()
        return {'message': f"Engrais #{pk} supprimé."}
