
#  services/sante_service.py


from django.core.exceptions import ValidationError
from django.utils import timezone
from ferme.models import SanteAnimal, Animal


class SanteService:

    @staticmethod
    def lister(animal_id=None, type_acte=None, date_debut=None, date_fin=None):
        qs = SanteAnimal.objects.select_related('animal').order_by('-date_evenement')
        if animal_id:
            qs = qs.filter(animal_id=animal_id)
        if type_acte:
            qs = qs.filter(type_acte=type_acte)
        if date_debut:
            qs = qs.filter(date_evenement__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_evenement__lte=date_fin)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return SanteAnimal.objects.select_related('animal').get(pk=pk)
        except SanteAnimal.DoesNotExist:
            raise ValidationError(f"Acte vétérinaire #{pk} introuvable.")

    @staticmethod
    def creer(data):
        animal_id = data.pop('animal_id', None) or data.pop('animal', None)
        if not animal_id:
            raise ValidationError("L'animal est obligatoire.")
        try:
            data['animal'] = Animal.objects.get(pk=animal_id)
        except Animal.DoesNotExist:
            raise ValidationError(f"Animal #{animal_id} introuvable.")
        soin = SanteAnimal(**data)
        soin.full_clean()
        soin.save()
        return soin

    @staticmethod
    def modifier(pk, data):
        soin = SanteService.obtenir(pk)
        if 'animal_id' in data or 'animal' in data:
            aid = data.pop('animal_id', None) or data.pop('animal', None)
            soin.animal = Animal.objects.get(pk=aid)
        for champ, valeur in data.items():
            setattr(soin, champ, valeur)
        soin.full_clean()
        soin.save()
        return soin

    @staticmethod
    def supprimer(pk):
        soin = SanteService.obtenir(pk)
        soin.delete()
        return {'message': f"Acte #{pk} supprimé."}

    @staticmethod
    def rdv_a_venir(jours=30):
        """Retourne les actes avec un prochain RDV dans les X prochains jours."""
        from datetime import timedelta
        aujourd_hui = timezone.now().date()
        limite = aujourd_hui + timedelta(days=jours)
        return (SanteAnimal.objects
                .select_related('animal')
                .filter(prochain_rdv__gte=aujourd_hui, prochain_rdv__lte=limite)
                .order_by('prochain_rdv'))

    @staticmethod
    def cout_total_par_animal(animal_id):
        """Calcule le coût vétérinaire total pour un animal."""
        soins = SanteAnimal.objects.filter(animal_id=animal_id)
        total = sum(s.cout_ariary for s in soins if s.cout_ariary)
        return {'animal_id': animal_id, 'cout_total_mga': total, 'nb_actes': soins.count()}
