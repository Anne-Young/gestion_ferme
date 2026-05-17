
#  views/enclos_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import EnclosService


def _serialize(e):
    return {
        'id':               e.pk,
        'nom_enclos':       e.nom_enclos,
        'type_enclos':      e.type_enclos,
        'capacite_max':     e.capacite_max,
        'superficie_m2':    float(e.superficie_m2) if e.superficie_m2 else None,
        'nb_animaux_actifs':e.nb_animaux_actifs,
        'taux_occupation':  e.taux_occupation,
    }


@csrf_exempt
@require_http_methods(["GET"])
def enclos_list(request):
    """GET /enclos/?type_enclos="""
    qs = EnclosService.lister(type_enclos=request.GET.get('type_enclos'))
    return JsonResponse([_serialize(e) for e in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def enclos_create(request):
    """POST /enclos/create/"""
    try:
        data   = json.loads(request.body)
        enclos = EnclosService.creer(data)
        return JsonResponse(_serialize(enclos), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def enclos_detail(request, pk):
    """GET /enclos/<pk>/"""
    try:
        return JsonResponse(_serialize(EnclosService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def enclos_update(request, pk):
    """PUT /enclos/<pk>/update/"""
    try:
        data   = json.loads(request.body)
        enclos = EnclosService.modifier(pk, data)
        return JsonResponse(_serialize(enclos))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def enclos_delete(request, pk):
    """DELETE /enclos/<pk>/delete/"""
    try:
        return JsonResponse(EnclosService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def enclos_occupation(request, pk):
    """GET /enclos/<pk>/occupation/"""
    try:
        return JsonResponse(EnclosService.taux_occupation(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)
