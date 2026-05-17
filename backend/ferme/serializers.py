# ============================================================
#  serializers.py — Ferme Fianarantsoa, Madagascar
# ============================================================

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Utilisateur, Espece, Race, Enclos, Animal,
    TypeAliment, StockAliment, Production, StockProduit,
    Vente, Engrais, AlimentationAnimal, SanteAnimal, Reproduction
)


# ============================================================
# AUTH
# ============================================================

class LoginSerializer(serializers.Serializer):
    login    = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['login'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Login ou mot de passe incorrect.")
        if not user.actif:
            raise serializers.ValidationError("Ce compte est désactivé.")
        data['user'] = user
        return data


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Utilisateur
        fields = ['id', 'nom_complet', 'login', 'role', 'telephone', 'actif']
        read_only_fields = ['id']


class UtilisateurCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = Utilisateur
        fields = ['nom_complet', 'login', 'password', 'role', 'telephone']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    ancien_mot_de_passe  = serializers.CharField(write_only=True)
    nouveau_mot_de_passe = serializers.CharField(write_only=True, min_length=6)

    def validate_ancien_mot_de_passe(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value


# ============================================================
# ESPECE & RACE
# ============================================================

class EspeceSerializer(serializers.ModelSerializer):
    nb_races = serializers.SerializerMethodField()

    class Meta:
        model  = Espece
        fields = ['id', 'nom_espece', 'description', 'nb_races']

    def get_nb_races(self, obj):
        return obj.races.count()


class RaceSerializer(serializers.ModelSerializer):
    espece_nom = serializers.CharField(source='espece.nom_espece', read_only=True)

    class Meta:
        model  = Race
        fields = ['id', 'espece', 'espece_nom', 'nom_race', 'aptitude', 'description']


# ============================================================
# ENCLOS
# ============================================================

class EnclosSerializer(serializers.ModelSerializer):
    nb_animaux_actifs = serializers.ReadOnlyField()
    taux_occupation   = serializers.ReadOnlyField()

    class Meta:
        model  = Enclos
        fields = [
            'id', 'nom_enclos', 'type_enclos', 'capacite_max',
            'superficie_m2', 'nb_animaux_actifs', 'taux_occupation'
        ]


# ============================================================
# ANIMAL
# ============================================================

class AnimalListSerializer(serializers.ModelSerializer):
    """Serializer allégé pour les listes (performance)"""
    race_nom   = serializers.CharField(source='race.nom_race', read_only=True)
    espece_nom = serializers.CharField(source='race.espece.nom_espece', read_only=True)
    enclos_nom = serializers.CharField(source='enclos.nom_enclos', read_only=True)

    class Meta:
        model  = Animal
        fields = [
            'id', 'num_identification', 'nom_local', 'sexe',
            'race_nom', 'espece_nom', 'enclos_nom',
            'statut', 'poids_kg', 'date_acquisition'
        ]


class AnimalDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour la fiche animal"""
    race_nom   = serializers.CharField(source='race.nom_race', read_only=True)
    espece_nom = serializers.CharField(source='race.espece.nom_espece', read_only=True)
    enclos_nom = serializers.CharField(source='enclos.nom_enclos', read_only=True)

    class Meta:
        model  = Animal
        fields = [
            'id', 'num_identification', 'nom_local', 'sexe',
            'race', 'race_nom', 'espece_nom',
            'enclos', 'enclos_nom',
            'date_naissance', 'date_acquisition', 'poids_kg',
            'statut', 'origine', 'observations'
        ]


class AnimalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Animal
        fields = [
            'num_identification', 'nom_local', 'sexe', 'race', 'enclos',
            'date_naissance', 'date_acquisition', 'poids_kg', 'origine', 'observations'
        ]

    def validate_num_identification(self, value):
        if Animal.objects.filter(num_identification=value).exists():
            raise serializers.ValidationError("Ce numéro d'identification existe déjà.")
        return value


# ============================================================
# TYPE ALIMENT & STOCK ALIMENT
# ============================================================

class TypeAlimentSerializer(serializers.ModelSerializer):
    stock_disponible = serializers.SerializerMethodField()
    en_alerte        = serializers.SerializerMethodField()

    class Meta:
        model  = TypeAliment
        fields = [
            'id', 'nom', 'categorie', 'unite_mesure',
            'cout_unitaire_ariary', 'origine',
            'stock_disponible', 'en_alerte'
        ]

    def get_stock_disponible(self, obj):
        try:
            return float(obj.stock.quantite_disponible)
        except StockAliment.DoesNotExist:
            return 0

    def get_en_alerte(self, obj):
        try:
            return obj.stock.en_alerte
        except StockAliment.DoesNotExist:
            return False


class StockAlimentSerializer(serializers.ModelSerializer):
    type_aliment_nom = serializers.CharField(source='type_aliment.nom', read_only=True)
    unite            = serializers.CharField(source='type_aliment.unite_mesure', read_only=True)
    en_alerte        = serializers.ReadOnlyField()

    class Meta:
        model  = StockAliment
        fields = [
            'id', 'type_aliment', 'type_aliment_nom', 'unite',
            'quantite_disponible', 'seuil_alerte', 'en_alerte', 'date_maj'
        ]


# ============================================================
# PRODUCTION
# ============================================================

class ProductionSerializer(serializers.ModelSerializer):
    animal_num  = serializers.CharField(source='animal.num_identification', read_only=True)
    enclos_nom  = serializers.CharField(source='enclos.nom_enclos', read_only=True)

    class Meta:
        model  = Production
        fields = [
            'id', 'animal', 'animal_num', 'enclos', 'enclos_nom',
            'type_produit', 'date_collecte', 'quantite', 'unite',
            'qualite', 'observations'
        ]

    def validate(self, data):
        if not data.get('animal') and not data.get('enclos'):
            raise serializers.ValidationError(
                "Précisez un animal ou un enclos pour cette production."
            )
        return data


# ============================================================
# STOCK PRODUIT
# ============================================================

class StockProduitSerializer(serializers.ModelSerializer):
    en_alerte = serializers.ReadOnlyField()

    class Meta:
        model  = StockProduit
        fields = [
            'id', 'type_produit', 'quantite_disponible',
            'unite', 'seuil_alerte', 'en_alerte', 'date_maj'
        ]


# ============================================================
# VENTE
# ============================================================

class VenteSerializer(serializers.ModelSerializer):
    montant_total = serializers.ReadOnlyField()

    class Meta:
        model  = Vente
        fields = [
            'id', 'type_produit', 'quantite_vendue', 'unite',
            'prix_unitaire_ariary', 'montant_total',
            'date_vente', 'acheteur', 'observations'
        ]

    def validate_quantite_vendue(self, value):
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être supérieure à 0.")
        return value

    def validate_prix_unitaire_ariary(self, value):
        if value < 0:
            raise serializers.ValidationError("Le prix ne peut pas être négatif.")
        return value


# ============================================================
# ENGRAIS
# ============================================================

class EngraisSerializer(serializers.ModelSerializer):
    enclos_nom = serializers.CharField(source='enclos.nom_enclos', read_only=True)

    class Meta:
        model  = Engrais
        fields = [
            'id', 'enclos', 'enclos_nom', 'type_engrais',
            'date_collecte', 'quantite_kg', 'statut_traitement',
            'date_disponibilite'
        ]


# ============================================================
# ALIMENTATION ANIMAL
# ============================================================

class AlimentationAnimalSerializer(serializers.ModelSerializer):
    animal_num       = serializers.CharField(source='animal.num_identification', read_only=True)
    enclos_nom       = serializers.CharField(source='enclos.nom_enclos', read_only=True)
    aliment_nom      = serializers.CharField(source='type_aliment.nom', read_only=True)
    cout_total_mga   = serializers.SerializerMethodField()

    class Meta:
        model  = AlimentationAnimal
        fields = [
            'id', 'animal', 'animal_num', 'enclos', 'enclos_nom',
            'type_aliment', 'aliment_nom',
            'date_distribution', 'quantite', 'unite',
            'responsable', 'cout_total_mga'
        ]

    def get_cout_total_mga(self, obj):
        cout = obj.type_aliment.cout_unitaire_ariary
        if cout is not None:
            return round(float(cout) * float(obj.quantite), 2)
        return None

    def validate(self, data):
        if not data.get('animal') and not data.get('enclos'):
            raise serializers.ValidationError(
                "Précisez un animal ou un enclos pour la distribution."
            )
        return data


# ============================================================
# SANTE ANIMAL
# ============================================================

class SanteAnimalSerializer(serializers.ModelSerializer):
    animal_num = serializers.CharField(source='animal.num_identification', read_only=True)

    class Meta:
        model  = SanteAnimal
        fields = [
            'id', 'animal', 'animal_num', 'date_evenement',
            'type_acte', 'description', 'medicament_utilise',
            'cout_ariary', 'veterinaire', 'prochain_rdv'
        ]


# ============================================================
# REPRODUCTION
# ============================================================

class ReproductionSerializer(serializers.ModelSerializer):
    mere_num = serializers.CharField(source='mere.num_identification', read_only=True)
    pere_num = serializers.CharField(source='pere.num_identification', read_only=True)

    class Meta:
        model  = Reproduction
        fields = [
            'id', 'mere', 'mere_num', 'pere', 'pere_num',
            'date_saillie', 'date_naissance',
            'nb_naissances', 'nb_survivants', 'observations'
        ]


# ============================================================
# DASHBOARD — Serializers de synthèse
# ============================================================

class DashboardSerializer(serializers.Serializer):
    """Données agrégées pour le tableau de bord"""
    nb_animaux_actifs     = serializers.IntegerField()
    nb_bovins             = serializers.IntegerField()
    nb_porcins            = serializers.IntegerField()
    nb_volailles          = serializers.IntegerField()
    productions_aujourd_hui = serializers.ListField()
    alertes_stock_aliment = serializers.ListField()
    alertes_stock_produit = serializers.ListField()
    rdv_veterinaires      = serializers.ListField()
    recettes_mois_mga     = serializers.DecimalField(max_digits=14, decimal_places=2)
