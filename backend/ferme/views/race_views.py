
#  views/race_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import RaceService


def _serialize(r):
    return {
        'id':          r.pk,
        'nom_race':    r.nom_race,
        'aptitude':    r.aptitude,
        'description': r.description,
        'espece': {
            'id':         r.espece.pk,
            'nom_espece': r.espece.nom_espece,
        },
    }


@csrf_exempt
@require_http_methods(["GET"])
def race_list(request):
    """GET/api/races/?espece_id=&aptitude="""
    qs = RaceService.lister(
        espece_id=request.GET.get('espece_id'),
        aptitude=request.GET.get('aptitude'),
    )
    return JsonResponse([_serialize(r) for r in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def race_create(request):
    """POST /races/create/"""
    try:
        data = json.loads(request.body)
        race = RaceService.creer(data)
        return JsonResponse(_serialize(race), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def race_detail(request, pk):
    """GET /races/<pk>/"""
    try:
        return JsonResponse(_serialize(RaceService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def race_update(request, pk):
    """PUT /races/<pk>/update/"""
    try:
        data = json.loads(request.body)
        race = RaceService.modifier(pk, data)
        return JsonResponse(_serialize(race))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def race_delete(request, pk):
    """DELETE /races/<pk>/delete/"""
    try:
        return JsonResponse(RaceService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
