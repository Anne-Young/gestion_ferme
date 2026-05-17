# ============================================================
#  models.py — Ferme Fianarantsoa, Madagascar
#  App Django : ferme
# ============================================================

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ============================================================
# GESTIONNAIRE UTILISATEUR PERSONNALISÉ
# ============================================================

class UtilisateurManager(BaseUserManager):
    def create_user(self, login, nom_complet, password=None, **extra_fields):
        if not login:
            raise ValueError("Le login est obligatoire")
        user = self.model(login=login, nom_complet=nom_complet, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, nom_complet, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, nom_complet, password, **extra_fields)


# ============================================================
# 1. UTILISATEUR
# ============================================================

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('gerant', 'Gérant'),
        ('employe', 'Employé'),
    ]

    nom_complet = models.CharField(max_length=100)
    login       = models.CharField(max_length=50, unique=True)
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employe')
    telephone   = models.CharField(max_length=15, blank=True, null=True,
                                   help_text="Numéro Telma / Airtel / Orange MG")
    actif       = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)

    USERNAME_FIELD  = 'login'
    REQUIRED_FIELDS = ['nom_complet']

    objects = UtilisateurManager()

    class Meta:
        db_table  = 'utilisateur'
        verbose_name = 'Utilisateur'

    def __str__(self):
        return f"{self.nom_complet} ({self.role})"


# ============================================================
# 2. ESPECE
# ============================================================

class Espece(models.Model):
    nom_espece  = models.CharField(max_length=50, unique=True,
                                   help_text="Ex : Bovin, Porcin, Volaille")
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'espece'
        verbose_name = 'Espèce'

    def __str__(self):
        return self.nom_espece


# ============================================================
# 3. RACE
# ============================================================

class Race(models.Model):
    APTITUDE_CHOICES = [
        ('lait',    'Lait'),
        ('viande',  'Viande'),
        ('mixte',   'Mixte'),
        ('ponte',   'Ponte'),
        ('chair',   'Chair'),
        ('engrais', 'Engrais'),
    ]

    espece      = models.ForeignKey(Espece, on_delete=models.RESTRICT,
                                    related_name='races')
    nom_race    = models.CharField(max_length=80,
                                   help_text="Ex : Zébu malgache, Large White, Rhode Island")
    aptitude    = models.CharField(max_length=10, choices=APTITUDE_CHOICES)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'race'
        verbose_name = 'Race'

    def __str__(self):
        return f"{self.nom_race} ({self.espece.nom_espece})"


# ============================================================
# 4. ENCLOS
# ============================================================

class Enclos(models.Model):
    TYPE_CHOICES = [
        ('etable',     'Étable'),
        ('porcherie',  'Porcherie'),
        ('poulailler', 'Poulailler'),
        ('parc',       'Parc'),
        ('paddock',    'Paddock'),
    ]

    nom_enclos    = models.CharField(max_length=50,
                                     help_text="Ex : Étable Nord, Porcherie A")
    type_enclos   = models.CharField(max_length=15, choices=TYPE_CHOICES)
    capacite_max  = models.PositiveIntegerField(help_text="Nombre maximum d'animaux")
    superficie_m2 = models.DecimalField(max_digits=7, decimal_places=2,
                                        blank=True, null=True)

    class Meta:
        db_table = 'enclos'
        verbose_name = 'Enclos'
        verbose_name_plural = 'Enclos'

    def __str__(self):
        return f"{self.nom_enclos} ({self.type_enclos})"

    @property
    def nb_animaux_actifs(self):
        return self.animaux.filter(statut='actif').count()

    @property
    def taux_occupation(self):
        if self.capacite_max > 0:
            return round((self.nb_animaux_actifs / self.capacite_max) * 100, 1)
        return 0


# ============================================================
# 5. ANIMAL
# ============================================================

class Animal(models.Model):
    SEXE_CHOICES = [('M', 'Mâle'), ('F', 'Femelle')]
    STATUT_CHOICES = [
        ('actif',   'Actif'),
        ('vendu',   'Vendu'),
        ('mort',    'Mort'),
        ('reforme', 'Réformé'),
    ]
    ORIGINE_CHOICES = [
        ('naissance_ferme', 'Naissance dans la ferme'),
        ('achat',           'Achat'),
        ('don',             'Don'),
    ]

    race             = models.ForeignKey(Race, on_delete=models.RESTRICT,
                                         related_name='animaux')
    enclos           = models.ForeignKey(Enclos, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='animaux')
    num_identification = models.CharField(max_length=30, unique=True,
                                          help_text="Matricule / numéro de boucle")
    nom_local        = models.CharField(max_length=60, blank=True, null=True,
                                        help_text="Nom vernaculaire donné par l'éleveur")
    sexe             = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance   = models.DateField(blank=True, null=True)
    date_acquisition = models.DateField()
    poids_kg         = models.DecimalField(max_digits=6, decimal_places=2,
                                           blank=True, null=True)
    statut           = models.CharField(max_length=10, choices=STATUT_CHOICES,
                                        default='actif')
    origine          = models.CharField(max_length=20, choices=ORIGINE_CHOICES)
    observations     = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'animal'
        verbose_name = 'Animal'

    def __str__(self):
        return f"{self.num_identification} — {self.race.nom_race}"

    @property
    def espece(self):
        return self.race.espece.nom_espece


# ============================================================
# 6. TYPE ALIMENT
# ============================================================

class TypeAliment(models.Model):
    CATEGORIE_CHOICES = [
        ('fourrage',   'Fourrage'),
        ('concentre',  'Concentré'),
        ('mineraux',   'Minéraux'),
        ('eau',        'Eau'),
        ('complement', 'Complément'),
    ]
    UNITE_CHOICES = [
        ('kg',    'Kilogramme'),
        ('litre', 'Litre'),
        ('botte', 'Botte'),
        ('sac',   'Sac'),
    ]
    ORIGINE_CHOICES = [
        ('produit_ferme', 'Produit dans la ferme'),
        ('achat_marche',  'Acheté au marché'),
    ]

    nom                  = models.CharField(max_length=80, unique=True,
                                            help_text="Ex : Herbe, Son de riz, Maïs, Eau")
    categorie            = models.CharField(max_length=15, choices=CATEGORIE_CHOICES)
    unite_mesure         = models.CharField(max_length=10, choices=UNITE_CHOICES)
    cout_unitaire_ariary = models.DecimalField(max_digits=8, decimal_places=2,
                                               blank=True, null=True,
                                               help_text="Coût moyen en Ariary (MGA)")
    origine              = models.CharField(max_length=20, choices=ORIGINE_CHOICES,
                                            blank=True, null=True)

    class Meta:
        db_table = 'type_aliment'
        verbose_name = 'Type d\'aliment'

    def __str__(self):
        return f"{self.nom} ({self.categorie})"


# ============================================================
# 7. STOCK ALIMENT
# ============================================================

class StockAliment(models.Model):
    type_aliment        = models.OneToOneField(TypeAliment, on_delete=models.RESTRICT,
                                               related_name='stock')
    quantite_disponible = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    seuil_alerte        = models.DecimalField(max_digits=8, decimal_places=2,
                                              blank=True, null=True)
    date_maj            = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_aliment'
        verbose_name = 'Stock aliment'

    def __str__(self):
        return f"Stock {self.type_aliment.nom} : {self.quantite_disponible}"

    @property
    def en_alerte(self):
        if self.seuil_alerte is not None:
            return self.quantite_disponible <= self.seuil_alerte
        return False


# ============================================================
# 8. PRODUCTION
# ============================================================

class Production(models.Model):
    TYPE_PRODUIT_CHOICES = [
        ('lait',       'Lait'),
        ('viande',     'Viande'),
        ('oeuf',       'Œuf'),
        ('fumier_brut','Fumier brut'),
    ]
    UNITE_CHOICES = [
        ('litre', 'Litre'),
        ('kg',    'Kilogramme'),
        ('unite', 'Unité'),
    ]
    QUALITE_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]

    animal        = models.ForeignKey(Animal, on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='productions')
    enclos        = models.ForeignKey(Enclos, on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='productions')
    type_produit  = models.CharField(max_length=15, choices=TYPE_PRODUIT_CHOICES)
    date_collecte = models.DateField()
    quantite      = models.DecimalField(max_digits=8, decimal_places=2)
    unite         = models.CharField(max_length=10, choices=UNITE_CHOICES)
    qualite       = models.CharField(max_length=1, choices=QUALITE_CHOICES,
                                     blank=True, null=True)
    observations  = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'production'
        verbose_name = 'Production'
        ordering = ['-date_collecte']

    def __str__(self):
        return f"{self.type_produit} — {self.quantite} {self.unite} ({self.date_collecte})"


# ============================================================
# 9. STOCK PRODUIT
# ============================================================

class StockProduit(models.Model):
    TYPE_CHOICES = [
        ('lait',          'Lait'),
        ('viande',        'Viande'),
        ('oeuf',          'Œuf'),
        ('engrais_traite','Engrais traité'),
    ]
    UNITE_CHOICES = [
        ('litre', 'Litre'),
        ('kg',    'Kilogramme'),
        ('unite', 'Unité'),
        ('sac',   'Sac'),
    ]

    type_produit        = models.CharField(max_length=15, choices=TYPE_CHOICES, unique=True)
    quantite_disponible = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    unite               = models.CharField(max_length=10, choices=UNITE_CHOICES)
    date_maj            = models.DateTimeField(auto_now=True)
    seuil_alerte        = models.DecimalField(max_digits=8, decimal_places=2,
                                              blank=True, null=True)

    class Meta:
        db_table = 'stock_produit'
        verbose_name = 'Stock produit'

    def __str__(self):
        return f"Stock {self.type_produit} : {self.quantite_disponible} {self.unite}"

    @property
    def en_alerte(self):
        if self.seuil_alerte is not None:
            return self.quantite_disponible <= self.seuil_alerte
        return False


# ============================================================
# 10. VENTE
# ============================================================

class Vente(models.Model):
    TYPE_CHOICES = [
        ('lait',          'Lait'),
        ('viande',        'Viande'),
        ('oeuf',          'Œuf'),
        ('engrais',       'Engrais'),
        ('animal_vivant', 'Animal vivant'),
    ]
    UNITE_CHOICES = [
        ('litre', 'Litre'),
        ('kg',    'Kilogramme'),
        ('unite', 'Unité'),
        ('sac',   'Sac'),
        ('tete',  'Tête'),
    ]

    type_produit         = models.CharField(max_length=15, choices=TYPE_CHOICES)
    quantite_vendue      = models.DecimalField(max_digits=8, decimal_places=2)
    unite                = models.CharField(max_length=10, choices=UNITE_CHOICES)
    prix_unitaire_ariary = models.DecimalField(max_digits=10, decimal_places=2,
                                               help_text="Prix en Ariary (MGA)")
    date_vente           = models.DateField()
    acheteur             = models.CharField(max_length=100, blank=True, null=True)
    observations         = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'vente'
        verbose_name = 'Vente'
        ordering = ['-date_vente']

    def __str__(self):
        return f"Vente {self.type_produit} — {self.montant_total} MGA ({self.date_vente})"

    @property
    def montant_total(self):
        return round(float(self.quantite_vendue) * float(self.prix_unitaire_ariary), 2)


# ============================================================
# 11. ENGRAIS
# ============================================================

class Engrais(models.Model):
    TYPE_CHOICES = [
        ('fumier_bovin',    'Fumier bovin'),
        ('fumier_porcin',   'Fumier porcin'),
        ('fiente_volaille', 'Fiente de volaille'),
        ('compost',         'Compost'),
    ]
    STATUT_CHOICES = [
        ('brut',          'Brut'),
        ('en_compostage', 'En compostage'),
        ('traite',        'Traité'),
        ('vendu',         'Vendu'),
    ]

    enclos             = models.ForeignKey(Enclos, on_delete=models.SET_NULL,
                                           null=True, blank=True, related_name='engrais')
    type_engrais       = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_collecte      = models.DateField()
    quantite_kg        = models.DecimalField(max_digits=8, decimal_places=2)
    statut_traitement  = models.CharField(max_length=15, choices=STATUT_CHOICES,
                                          default='brut')
    date_disponibilite = models.DateField(blank=True, null=True,
                                          help_text="Date prévue fin de compostage")

    class Meta:
        db_table = 'engrais'
        verbose_name = 'Engrais'
        verbose_name_plural = 'Engrais'
        ordering = ['-date_collecte']

    def __str__(self):
        return f"{self.type_engrais} — {self.quantite_kg} kg ({self.statut_traitement})"


# ============================================================
# 12. ALIMENTATION ANIMAL
# ============================================================

class AlimentationAnimal(models.Model):
    UNITE_CHOICES = [
        ('kg',    'Kilogramme'),
        ('litre', 'Litre'),
        ('botte', 'Botte'),
    ]

    animal            = models.ForeignKey(Animal, on_delete=models.SET_NULL,
                                          null=True, blank=True,
                                          related_name='alimentations',
                                          help_text="Ration individuelle")
    enclos            = models.ForeignKey(Enclos, on_delete=models.SET_NULL,
                                          null=True, blank=True,
                                          related_name='alimentations',
                                          help_text="Ration groupée par enclos")
    type_aliment      = models.ForeignKey(TypeAliment, on_delete=models.RESTRICT,
                                          related_name='distributions')
    date_distribution = models.DateTimeField()
    quantite          = models.DecimalField(max_digits=7, decimal_places=2)
    unite             = models.CharField(max_length=10, choices=UNITE_CHOICES)
    responsable       = models.CharField(max_length=80, blank=True, null=True,
                                         help_text="Nom de l'employé ou éleveur")

    class Meta:
        db_table = 'alimentation_animal'
        verbose_name = 'Distribution alimentaire'
        ordering = ['-date_distribution']

    def __str__(self):
        cible = self.animal or self.enclos
        return f"{self.type_aliment.nom} → {cible} ({self.date_distribution.date()})"


# ============================================================
# 13. SANTE ANIMAL
# ============================================================

class SanteAnimal(models.Model):
    TYPE_ACTE_CHOICES = [
        ('vaccination', 'Vaccination'),
        ('traitement',  'Traitement'),
        ('vermifuge',   'Vermifuge'),
        ('pesee',       'Pesée'),
        ('controle',    'Contrôle'),
    ]

    animal            = models.ForeignKey(Animal, on_delete=models.CASCADE,
                                          related_name='soins')
    date_evenement    = models.DateField()
    type_acte         = models.CharField(max_length=15, choices=TYPE_ACTE_CHOICES)
    description       = models.TextField(blank=True, null=True)
    medicament_utilise = models.CharField(max_length=100, blank=True, null=True)
    cout_ariary       = models.DecimalField(max_digits=10, decimal_places=2,
                                            blank=True, null=True,
                                            help_text="Coût en MGA")
    veterinaire       = models.CharField(max_length=80, blank=True, null=True)
    prochain_rdv      = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'sante_animal'
        verbose_name = 'Acte vétérinaire'
        ordering = ['-date_evenement']

    def __str__(self):
        return f"{self.type_acte} — {self.animal} ({self.date_evenement})"


# ============================================================
# 14. REPRODUCTION
# ============================================================

class Reproduction(models.Model):
    mere           = models.ForeignKey(Animal, on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='naissances_mere')
    pere           = models.ForeignKey(Animal, on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='naissances_pere')
    date_saillie   = models.DateField(blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    nb_naissances  = models.PositiveSmallIntegerField(blank=True, null=True)
    nb_survivants  = models.PositiveSmallIntegerField(blank=True, null=True)
    observations   = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'reproduction'
        verbose_name = 'Reproduction'
        ordering = ['-date_naissance']

    def __str__(self):
        return f"Repro {self.mere} × {self.pere} — {self.date_naissance}"
