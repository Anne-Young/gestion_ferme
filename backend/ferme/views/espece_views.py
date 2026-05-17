
#  views/espece_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import EspeceService


def _serialize(e):
    return {
        'id':          e.pk,
        'nom_espece':  e.nom_espece,
        'description': e.description,
        'nb_races':    e.races.count(),
    }


@csrf_exempt
@require_http_methods(["GET"])
def espece_list(request):
    """GET /especes/"""
    qs = EspeceService.lister()
    return JsonResponse([_serialize(e) for e in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def espece_create(request):
    """POST /especes/create/"""
    try:
        data   = json.loads(request.body)
        espece = EspeceService.creer(data)
        return JsonResponse(_serialize(espece), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def espece_detail(request, pk):
    """GET /especes/<pk>/"""
    try:
        return JsonResponse(_serialize(EspeceService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def espece_update(request, pk):
    """PUT /especes/<pk>/update/"""
    try:
        data   = json.loads(request.body)
        espece = EspeceService.modifier(pk, data)
        return JsonResponse(_serialize(espece))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def espece_delete(request, pk):
    """DELETE /especes/<pk>/delete/"""
    try:
        return JsonResponse(EspeceService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
