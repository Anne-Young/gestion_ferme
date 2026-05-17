# ============================================================
#  views/animal_views.py
# ============================================================

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import AnimalService


def _serialize(a):
    return {
        'id':a.pk,
        'num_identification':a.num_identification,
        'nom_local':a.nom_local,
        'sexe':a.sexe,
        'statut':a.statut,
        'origine':a.origine,
        'date_naissance':str(a.date_naissance) if a.date_naissance else None,
        'date_acquisition':str(a.date_acquisition),
        'poids_kg':float(a.poids_kg) if a.poids_kg else None,
        'observations':a.observations,
        'espece':a.espece,
        'race': {
            'id':a.race.pk,
            'nom_race': a.race.nom_race,
            'aptitude': a.race.aptitude,
        },
        'enclos': {
            'id':a.enclos.pk,
            'nom_enclos': a.enclos.nom_enclos,
        } if a.enclos else None,
    }


@csrf_exempt
@require_http_methods(["GET"])
def animal_list(request):
    """GET /animaux/?statut=&sexe=&enclos_id=&race_id=&search="""
    qs = AnimalService.lister(
        statut= request.GET.get('statut'),
        sexe= request.GET.get('sexe'),
        enclos_id = request.GET.get('enclos_id'),
        race_id= request.GET.get('race_id'),
        search= request.GET.get('search'),
    )
    return JsonResponse([_serialize(a) for a in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def animal_create(request):
    """POST /animaux/create/"""
    try:
        data= json.loads(request.body)
        animal = AnimalService.creer(data)
        return JsonResponse(_serialize(animal), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def animal_detail(request, pk):
    """GET /animaux/<pk>/"""
    try:
        return JsonResponse(_serialize(AnimalService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def animal_update(request, pk):
    """PUT /animaux/<pk>/update/"""
    try:
        data = json.loads(request.body)
        animal = AnimalService.modifier(pk, data)
        return JsonResponse(_serialize(animal))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def animal_delete(request, pk):
    """DELETE /animaux/<pk>/delete/"""
    try:
        return JsonResponse(AnimalService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def animal_changer_statut(request, pk):
    """POST /animaux/<pk>/statut/ — body: {"statut": "vendu"}"""
    try:
        data= json.loads(request.body)
        statut = data.get('statut')
        return JsonResponse(AnimalService.changer_statut(pk, statut))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def animal_stats_espece(request):
    """GET /animaux/stats/espece/"""
    return JsonResponse(list(AnimalService.stats_par_espece()), safe=False)
