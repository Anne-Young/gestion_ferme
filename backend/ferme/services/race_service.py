
#  services/race_service.py


from django.core.exceptions import ValidationError
from ferme.models import Race, Espece


class RaceService:

    @staticmethod
    def lister(espece_id=None, aptitude=None):
        qs = Race.objects.select_related('espece').order_by('nom_race')
        if espece_id:
            qs = qs.filter(espece_id=espece_id)
        if aptitude:
            qs = qs.filter(aptitude=aptitude)
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return Race.objects.select_related('espece').get(pk=pk)
        except Race.DoesNotExist:
            raise ValidationError(f"Race #{pk} introuvable.")

    @staticmethod
    def creer(data):
        espece_id = data.get('espece_id') or data.get('espece')
        if not espece_id:
            raise ValidationError("L'espèce est obligatoire.")
        try:
            espece = Espece.objects.get(pk=espece_id)
        except Espece.DoesNotExist:
            raise ValidationError(f"Espèce #{espece_id} introuvable.")

        nom = data.get('nom_race', '').strip()
        if Race.objects.filter(nom_race__iexact=nom, espece=espece).exists():
            raise ValidationError(f"La race '{nom}' existe déjà pour '{espece.nom_espece}'.")

        data['espece'] = espece
        data.pop('espece_id', None)
        race = Race(**data)
        race.full_clean()
        race.save()
        return race

    @staticmethod
    def modifier(pk, data):
        race = RaceService.obtenir(pk)
        if 'espece_id' in data or 'espece' in data:
            espece_id = data.pop('espece_id', None) or data.pop('espece', None)
            race.espece = Espece.objects.get(pk=espece_id)
        for champ, valeur in data.items():
            setattr(race, champ, valeur)
        race.full_clean()
        race.save()
        return race

    @staticmethod
    def supprimer(pk):
        race = RaceService.obtenir(pk)
        if race.animaux.exists():
            raise ValidationError(
                f"Impossible de supprimer '{race.nom_race}' : des animaux y sont rattachés."
            )
        nom = race.nom_race
        race.delete()
        return {'message': f"Race '{nom}' supprimée."}
