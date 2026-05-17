
#  views/reproduction_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import ReproductionService


def _serialize(r):
    return {
        'id':             r.pk,
        'date_saillie':   str(r.date_saillie) if r.date_saillie else None,
        'date_naissance': str(r.date_naissance) if r.date_naissance else None,
        'nb_naissances':  r.nb_naissances,
        'nb_survivants':  r.nb_survivants,
        'observations':   r.observations,
        'mere': {'id': r.mere.pk, 'num': r.mere.num_identification} if r.mere else None,
        'pere': {'id': r.pere.pk, 'num': r.pere.num_identification} if r.pere else None,
    }


@csrf_exempt
@require_http_methods(["GET"])
def reproduction_list(request):
    """GET /reproductions/?mere_id=&pere_id=&date_debut=&date_fin="""
    qs = ReproductionService.lister(
        mere_id    = request.GET.get('mere_id'),
        pere_id    = request.GET.get('pere_id'),
        date_debut = request.GET.get('date_debut'),
        date_fin   = request.GET.get('date_fin'),
    )
    return JsonResponse([_serialize(r) for r in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def reproduction_create(request):
    """POST /reproductions/create/"""
    try:
        data  = json.loads(request.body)
        repro = ReproductionService.creer(data)
        return JsonResponse(_serialize(repro), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def reproduction_detail(request, pk):
    """GET /reproductions/<pk>/"""
    try:
        return JsonResponse(_serialize(ReproductionService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def reproduction_update(request, pk):
    """PUT /reproductions/<pk>/update/"""
    try:
        data  = json.loads(request.body)
        repro = ReproductionService.modifier(pk, data)
        return JsonResponse(_serialize(repro))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def reproduction_delete(request, pk):
    """DELETE/reproductions/<pk>/delete/"""
    try:
        return JsonResponse(ReproductionService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def reproduction_taux_survie(request):
    """GET /reproductions/taux-survie/"""
    return JsonResponse(ReproductionService.taux_survie_global())
