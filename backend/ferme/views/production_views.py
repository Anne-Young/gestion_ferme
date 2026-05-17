
#  views/production_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import ProductionService


def _serialize(p):
    return {
        'id':            p.pk,
        'type_produit':  p.type_produit,
        'date_collecte': str(p.date_collecte),
        'quantite':      float(p.quantite),
        'unite':         p.unite,
        'qualite':       p.qualite,
        'observations':  p.observations,
        'animal': {'id': p.animal.pk, 'num': p.animal.num_identification} if p.animal else None,
        'enclos': {'id': p.enclos.pk, 'nom': p.enclos.nom_enclos} if p.enclos else None,
    }


@csrf_exempt
@require_http_methods(["GET"])
def production_list(request):
    """GET /productions/?type_produit=&animal_id=&enclos_id=&date_debut=&date_fin="""
    qs = ProductionService.lister(
        type_produit = request.GET.get('type_produit'),
        animal_id    = request.GET.get('animal_id'),
        enclos_id    = request.GET.get('enclos_id'),
        date_debut   = request.GET.get('date_debut'),
        date_fin     = request.GET.get('date_fin'),
    )
    return JsonResponse([_serialize(p) for p in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def production_create(request):
    """POST /productions/create/"""
    try:
        data = json.loads(request.body)
        prod = ProductionService.creer(data)
        return JsonResponse(_serialize(prod), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def production_detail(request, pk):
    """GET /productions/<pk>/"""
    try:
        return JsonResponse(_serialize(ProductionService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def production_update(request, pk):
    """PUT /productions/<pk>/update/"""
    try:
        data = json.loads(request.body)
        prod = ProductionService.modifier(pk, data)
        return JsonResponse(_serialize(prod))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def production_delete(request, pk):
    """DELETE /productions/<pk>/delete/"""
    try:
        return JsonResponse(ProductionService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def production_totaux(request):
    """GET /productions/totaux/?date_debut=&date_fin="""
    result = ProductionService.totaux_par_type(
        date_debut=request.GET.get('date_debut'),
        date_fin=request.GET.get('date_fin'),
    )
    return JsonResponse(list(result), safe=False)
