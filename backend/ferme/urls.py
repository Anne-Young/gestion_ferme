
from django.urls import path
from ferme.views import (
    # ── Authentification ──────────────────────────
    utilisateur_login,

    # ── Utilisateurs ──────────────────────────────
    utilisateur_list, utilisateur_create,
    utilisateur_detail, utilisateur_update, utilisateur_delete,
    utilisateur_toggle_actif,

    # ── Espèces ───────────────────────────────────
    espece_list, espece_create,
    espece_detail, espece_update, espece_delete,

    # ── Races ─────────────────────────────────────
    race_list, race_create,
    race_detail, race_update, race_delete,

    # ── Enclos ────────────────────────────────────
    enclos_list, enclos_create,
    enclos_detail, enclos_update, enclos_delete,
    enclos_occupation,

    # ── Animaux ───────────────────────────────────
    animal_list, animal_create,
    animal_detail, animal_update, animal_delete,
    animal_changer_statut, animal_stats_espece,

    # ── Types d'aliments ──────────────────────────
    type_aliment_list, type_aliment_create,
    type_aliment_detail, type_aliment_update, type_aliment_delete,

    # ── Stocks aliments ───────────────────────────
    stock_aliment_list, stock_aliment_create,
    stock_aliment_detail, stock_aliment_update, stock_aliment_delete,
    stock_aliment_ajouter, stock_aliment_retirer,

    # ── Productions ───────────────────────────────
    production_list, production_create,
    production_detail, production_update, production_delete,
    production_totaux,

    # ── Stocks produits ───────────────────────────
    stock_produit_list, stock_produit_create,
    stock_produit_detail, stock_produit_update, stock_produit_delete,
    stock_produit_ajouter, stock_produit_retirer,

    # ── Ventes ────────────────────────────────────
    vente_list, vente_create,
    vente_detail, vente_update, vente_delete,
    vente_chiffre_affaires,

    # ── Engrais ───────────────────────────────────
    engrais_list, engrais_create,
    engrais_detail, engrais_update, engrais_delete,
    engrais_changer_statut,

    # ── Alimentation ──────────────────────────────
    alimentation_list, alimentation_create,
    alimentation_detail, alimentation_update, alimentation_delete,

    # ── Santé ─────────────────────────────────────
    sante_list, sante_create,
    sante_detail, sante_update, sante_delete,
    sante_rdv_a_venir, sante_cout_animal,

    # ── Reproduction ──────────────────────────────
    reproduction_list, reproduction_create,
    reproduction_detail, reproduction_update, reproduction_delete,
    reproduction_taux_survie,
)

app_name = 'ferme'

urlpatterns = [


    # AUTH

    path('auth/login/',utilisateur_login,name='auth-login'),


    # UTILISATEURS

    path('utilisateurs/',utilisateur_list,name='utilisateur-list'),
    path('utilisateurs/create/', utilisateur_create,name='utilisateur-create'),
    path('utilisateurs/<int:pk>/',utilisateur_detail,name='utilisateur-detail'),
    path('utilisateurs/<int:pk>/update/',utilisateur_update,name='utilisateur-update'),
    path('utilisateurs/<int:pk>/delete/',utilisateur_delete,name='utilisateur-delete'),
    path('utilisateurs/<int:pk>/toggle-actif/',utilisateur_toggle_actif,name='utilisateur-toggle'),

    # ESPÈCES

    path('especes/',espece_list,name='espece-list'),
    path('especes/create/',espece_create,name='espece-create'),
    path('especes/<int:pk>/',espece_detail,name='espece-detail'),
    path('especes/<int:pk>/update/',espece_update,name='espece-update'),
    path('especes/<int:pk>/delete/',espece_delete,name='espece-delete'),

    # RACES

    path('races/',race_list,name='race-list'),
    path('races/create/',race_create,name='race-create'),
    path('races/<int:pk>/',race_detail,name='race-detail'),
    path('races/<int:pk>/update/',race_update,name='race-update'),
    path('races/<int:pk>/delete/',race_delete,name='race-delete'),


    # ENCLOS

    path('enclos/',enclos_list,name='enclos-list'),
    path('enclos/create/', enclos_create,name='enclos-create'),
    path('enclos/<int:pk>/',enclos_detail, name='enclos-detail'),
    path('enclos/<int:pk>/update/',enclos_update,name='enclos-update'),
    path('enclos/<int:pk>/delete/',enclos_delete,name='enclos-delete'),
    path('enclos/<int:pk>/occupation/', enclos_occupation,name='enclos-occupation'),

 
    # ANIMAUX

    path('animaux/',animal_list,name='animal-list'),
    path('animaux/create/', animal_create,name='animal-create'),
    path('animaux/stats/espece/',animal_stats_espece,name='animal-stats-espece'),
    path('animaux/<int:pk>/',animal_detail,name='animal-detail'),
    path('animaux/<int:pk>/update/',animal_update, name='animal-update'),
    path('animaux/<int:pk>/delete/',animal_delete,name='animal-delete'),
    path('animaux/<int:pk>/statut/',animal_changer_statut,name='animal-statut'),


    # TYPES D'ALIMENTS

    path('aliments/',type_aliment_list,name='aliment-list'),
    path('aliments/create/',type_aliment_create,name='aliment-create'),
    path('aliments/<int:pk>/',type_aliment_detail,name='aliment-detail'),
    path('aliments/<int:pk>/update/',type_aliment_update,        name='aliment-update'),
    path('aliments/<int:pk>/delete/',type_aliment_delete, name='aliment-delete'),

    # STOCKS ALIMENTS
  
    path('stocks/aliments/',stock_aliment_list,name='stock-aliment-list'),
    path('stocks/aliments/create/',stock_aliment_create,name='stock-aliment-create'),
    path('stocks/aliments/<int:pk>/',stock_aliment_detail,name='stock-aliment-detail'),
    path('stocks/aliments/<int:pk>/update/',stock_aliment_update,name='stock-aliment-update'),
    path('stocks/aliments/<int:pk>/delete/',stock_aliment_delete,name='stock-aliment-delete'),
    path('stocks/aliments/<int:pk>/ajouter/',stock_aliment_ajouter,name='stock-aliment-ajouter'),
    path('stocks/aliments/<int:pk>/retirer/',stock_aliment_retirer,name='stock-aliment-retirer'),


    # PRODUCTIONS
    
    path('productions/',production_list,name='production-list'),
    path('productions/create/',production_create,name='production-create'),
    path('productions/totaux/',production_totaux,name='production-totaux'),
    path('productions/<int:pk>/',production_detail,name='production-detail'),
    path('productions/<int:pk>/update/',production_update,name='production-update'),
    path('productions/<int:pk>/delete/',production_delete,name='production-delete'),


    # STOCKS PRODUITS
    
    path('stocks/produits/',stock_produit_list,name='stock-produit-list'),
    path('stocks/produits/create/',stock_produit_create,name='stock-produit-create'),
    path('stocks/produits/ajouter/',stock_produit_ajouter,name='stock-produit-ajouter'),
    path('stocks/produits/retirer/',stock_produit_retirer,name='stock-produit-retirer'),
    path('stocks/produits/<int:pk>/',stock_produit_detail,name='stock-produit-detail'),
    path('stocks/produits/<int:pk>/update/',stock_produit_update,name='stock-produit-update'),
    path('stocks/produits/<int:pk>/delete/',stock_produit_delete,name='stock-produit-delete'),

    # VENTES

    path('ventes/',vente_list, name='vente-list'),
    path('ventes/create/', vente_create,name='vente-create'),
    path('ventes/ca/',vente_chiffre_affaires,name='vente-ca'),
    path('ventes/<int:pk>/',vente_detail,name='vente-detail'),
    path('ventes/<int:pk>/update/',vente_update,name='vente-update'),
    path('ventes/<int:pk>/delete/',vente_delete, name='vente-delete'),

 
    # ENGRAIS

    path('engrais/',engrais_list,name='engrais-list'),
    path('engrais/create/',engrais_create,name='engrais-create'),
    path('engrais/<int:pk>/',engrais_detail,name='engrais-detail'),
    path('engrais/<int:pk>/update/',engrais_update, name='engrais-update'),
    path('engrais/<int:pk>/delete/',engrais_delete,name='engrais-delete'),
    path('engrais/<int:pk>/statut/',engrais_changer_statut,name='engrais-statut'),


    # ALIMENTATION
  
    path('alimentations/',alimentation_list,name='alimentation-list'),
    path('alimentations/create/',alimentation_create,name='alimentation-create'),
    path('alimentations/<int:pk>/',alimentation_detail,name='alimentation-detail'),
    path('alimentations/<int:pk>/update/',alimentation_update,name='alimentation-update'),
    path('alimentations/<int:pk>/delete/',alimentation_delete,name='alimentation-delete'),


        # SANTÉ ANIMALE

    path('sante/',sante_list,name='sante-list'),
    path('sante/create/',sante_create,name='sante-create'),
    path('sante/rdv/',sante_rdv_a_venir,name='sante-rdv'),
    path('sante/cout/<int:animal_id>/',sante_cout_animal,name='sante-cout'),
    path('sante/<int:pk>/',sante_detail,name='sante-detail'),
    path('sante/<int:pk>/update/',sante_update,name='sante-update'),
    path('sante/<int:pk>/delete/',sante_delete,name='sante-delete'),

    
    # REPRODUCTION
    
    path('reproductions/',reproduction_list,name='reproduction-list'),
    path('reproductions/create/',reproduction_create,name='reproduction-create'),
    path('reproductions/taux-survie/',reproduction_taux_survie,name='reproduction-taux'),
    path('reproductions/<int:pk>/',reproduction_detail,name='reproduction-detail'),
    path('reproductions/<int:pk>/update/',reproduction_update, name='reproduction-update'),
    path('reproductions/<int:pk>/delete/',reproduction_delete,name='reproduction-delete'),
]
