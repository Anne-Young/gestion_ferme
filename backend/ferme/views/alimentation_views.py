
#  views/alimentation_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import AlimentationService


def _serialize(d):
    return {
        'id':                d.pk,
        'date_distribution': d.date_distribution.isoformat(),
        'quantite':          float(d.quantite),
        'unite':             d.unite,
        'responsable':       d.responsable,
        'type_aliment': {
            'id':  d.type_aliment.pk,
            'nom': d.type_aliment.nom,
        },
        'animal': {'id': d.animal.pk, 'num': d.animal.num_identification} if d.animal else None,
        'enclos': {'id': d.enclos.pk, 'nom': d.enclos.nom_enclos} if d.enclos else None,
    }


@csrf_exempt
@require_http_methods(["GET"])
def alimentation_list(request):
    """GET /alimentations/?animal_id=&enclos_id=&type_aliment_id=&date_debut=&date_fin="""
    qs = AlimentationService.lister(
        animal_id      = request.GET.get('animal_id'),
        enclos_id      = request.GET.get('enclos_id'),
        type_aliment_id= request.GET.get('type_aliment_id'),
        date_debut     = request.GET.get('date_debut'),
        date_fin       = request.GET.get('date_fin'),
    )
    return JsonResponse([_serialize(d) for d in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def alimentation_create(request):
    """POST /alimentations/create/"""
    try:
        data    = json.loads(request.body)
        deduire = data.pop('deduire_stock', True)
        dist    = AlimentationService.creer(data, deduire_stock=deduire)
        return JsonResponse(_serialize(dist), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def alimentation_detail(request, pk):
    """GET /alimentations/<pk>/"""
    try:
        return JsonResponse(_serialize(AlimentationService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def alimentation_update(request, pk):
    """PUT /alimentations/<pk>/update/"""
    try:
        data = json.loads(request.body)
        dist = AlimentationService.modifier(pk, data)
        return JsonResponse(_serialize(dist))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def alimentation_delete(request, pk):
    """DELETE /alimentations/<pk>/delete/"""
    try:
        return JsonResponse(AlimentationService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
