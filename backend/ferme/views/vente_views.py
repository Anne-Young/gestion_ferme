
#  views/vente_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import VenteService


def _serialize(v):
    return {
        'id':v.pk,
        'type_produit':v.type_produit,
        'quantite_vendue':float(v.quantite_vendue),
        'unite': v.unite,
        'prix_unitaire_ariary':float(v.prix_unitaire_ariary),
        'montant_total':v.montant_total,
        'date_vente':str(v.date_vente),
        'acheteur':v.acheteur,
        'observations':v.observations,
    }


@csrf_exempt
@require_http_methods(["GET"])
def vente_list(request):
    """GET /ventes/?type_produit=&date_debut=&date_fin=&acheteur="""
    qs = VenteService.lister(
        type_produit = request.GET.get('type_produit'),
        date_debut= request.GET.get('date_debut'),
        date_fin= request.GET.get('date_fin'),
        acheteur= request.GET.get('acheteur'),
    )
    return JsonResponse([_serialize(v) for v in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def vente_create(request):
    """POST /ventes/create/"""
    try:
        data  = json.loads(request.body)
        deduire = data.pop('deduire_stock', True)
        vente = VenteService.creer(data, deduire_stock=deduire)
        return JsonResponse(_serialize(vente), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def vente_detail(request, pk):
    """GET /ventes/<pk>/"""
    try:
        return JsonResponse(_serialize(VenteService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def vente_update(request, pk):
    """PUT /ventes/<pk>/update/"""
    try:
        data  = json.loads(request.body)
        vente = VenteService.modifier(pk, data)
        return JsonResponse(_serialize(vente))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def vente_delete(request, pk):
    """DELETE /ventes/<pk>/delete/"""
    try:
        return JsonResponse(VenteService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def vente_chiffre_affaires(request):
    """GET /ventes/ca/?date_debut=&date_fin="""
    result = VenteService.chiffre_affaires(
        date_debut=request.GET.get('date_debut'),
        date_fin=request.GET.get('date_fin'),
    )
    return JsonResponse(result)
