
#  services/animal_service.py


from django.core.exceptions import ValidationError
from django.db.models import Q
from ferme.models import Animal, Race, Enclos


class AnimalService:

    @staticmethod
    def lister(statut=None, sexe=None, enclos_id=None, race_id=None, search=None):
        qs = (Animal.objects
              .select_related('race__espece', 'enclos')
              .order_by('num_identification'))
        if statut:
            qs = qs.filter(statut=statut)
        if sexe:
            qs = qs.filter(sexe=sexe)
        if enclos_id:
            qs = qs.filter(enclos_id=enclos_id)
        if race_id:
            qs = qs.filter(race_id=race_id)
        if search:
            qs = qs.filter(
                Q(num_identification__icontains=search) |
                Q(nom_local__icontains=search)
            )
        return qs

    @staticmethod
    def obtenir(pk):
        try:
            return Animal.objects.select_related('race__espece', 'enclos').get(pk=pk)
        except Animal.DoesNotExist:
            raise ValidationError(f"Animal #{pk} introuvable.")

    @staticmethod
    def creer(data):
        # Vérifier unicité du numéro d'identification
        num = data.get('num_identification', '').strip()
        if Animal.objects.filter(num_identification=num).exists():
            raise ValidationError(f"Le numéro '{num}' est déjà attribué.")

        # Résoudre FK race
        race_id = data.pop('race_id', None) or data.pop('race', None)
        if not race_id:
            raise ValidationError("La race est obligatoire.")
        try:
            data['race'] = Race.objects.get(pk=race_id)
        except Race.DoesNotExist:
            raise ValidationError(f"Race #{race_id} introuvable.")

        # Résoudre FK enclos (optionnel)
        enclos_id = data.pop('enclos_id', None) or data.pop('enclos', None)
        if enclos_id:
            try:
                enclos = Enclos.objects.get(pk=enclos_id)
                # Vérifier capacité
                if enclos.nb_animaux_actifs >= enclos.capacite_max:
                    raise ValidationError(
                        f"L'enclos '{enclos.nom_enclos}' est plein ({enclos.capacite_max} animaux max)."
                    )
                data['enclos'] = enclos
            except Enclos.DoesNotExist:
                raise ValidationError(f"Enclos #{enclos_id} introuvable.")

        animal = Animal(**data)
        animal.full_clean()
        animal.save()
        return animal

    @staticmethod
    def modifier(pk, data):
        animal = AnimalService.obtenir(pk)

        # Numéro d'identification unique
        num = data.get('num_identification', animal.num_identification).strip()
        if Animal.objects.filter(num_identification=num).exclude(pk=pk).exists():
            raise ValidationError(f"Le numéro '{num}' est déjà attribué.")

        # FK race
        if 'race_id' in data or 'race' in data:
            race_id = data.pop('race_id', None) or data.pop('race', None)
            animal.race = Race.objects.get(pk=race_id)

        # FK enclos
        if 'enclos_id' in data or 'enclos' in data:
            enclos_id = data.pop('enclos_id', None) or data.pop('enclos', None)
            if enclos_id:
                animal.enclos = Enclos.objects.get(pk=enclos_id)
            else:
                animal.enclos = None

        for champ, valeur in data.items():
            setattr(animal, champ, valeur)

        animal.full_clean()
        animal.save()
        return animal

    @staticmethod
    def supprimer(pk):
        animal = AnimalService.obtenir(pk)
        num = animal.num_identification
        animal.delete()
        return {'message': f"Animal '{num}' supprimé."}

    @staticmethod
    def changer_statut(pk, nouveau_statut):
        """Vente, mort, réforme d'un animal."""
        valides = [s[0] for s in Animal.STATUT_CHOICES]
        if nouveau_statut not in valides:
            raise ValidationError(f"Statut '{nouveau_statut}' invalide. Choix : {valides}")
        animal = AnimalService.obtenir(pk)
        animal.statut = nouveau_statut
        animal.save(update_fields=['statut'])
        return {'message': f"Animal '{animal.num_identification}' → statut '{nouveau_statut}'."}

    @staticmethod
    def stats_par_espece():
        """Retourne le nombre d'animaux actifs par espèce."""
        from django.db.models import Count
        return (Animal.objects
                .filter(statut='actif')
                .values('race__espece__nom_espece')
                .annotate(total=Count('id'))
                .order_by('-total'))
