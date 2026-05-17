
#  views/engrais_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import EngraisService


def _serialize(e):
    return {
        'id':                  e.pk,
        'type_engrais':        e.type_engrais,
        'date_collecte':       str(e.date_collecte),
        'quantite_kg':         float(e.quantite_kg),
        'statut_traitement':   e.statut_traitement,
        'date_disponibilite':  str(e.date_disponibilite) if e.date_disponibilite else None,
        'enclos': {'id': e.enclos.pk, 'nom': e.enclos.nom_enclos} if e.enclos else None,
    }


@csrf_exempt
@require_http_methods(["GET"])
def engrais_list(request):
    """GET/engrais/?statut=&type_engrais=&enclos_id="""
    qs = EngraisService.lister(
        statut       = request.GET.get('statut'),
        type_engrais = request.GET.get('type_engrais'),
        enclos_id    = request.GET.get('enclos_id'),
    )
    return JsonResponse([_serialize(e) for e in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def engrais_create(request):
    """POST /engrais/create/"""
    try:
        data    = json.loads(request.body)
        engrais = EngraisService.creer(data)
        return JsonResponse(_serialize(engrais), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def engrais_detail(request, pk):
    """GET /engrais/<pk>/"""
    try:
        return JsonResponse(_serialize(EngraisService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def engrais_update(request, pk):
    """PUT /engrais/<pk>/update/"""
    try:
        data    = json.loads(request.body)
        engrais = EngraisService.modifier(pk, data)
        return JsonResponse(_serialize(engrais))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def engrais_delete(request, pk):
    """DELETE /engrais/<pk>/delete/"""
    try:
        return JsonResponse(EngraisService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def engrais_changer_statut(request, pk):
    """POST /engrais/<pk>/statut/ — body: {"statut": "en_compostage"}"""
    try:
        data    = json.loads(request.body)
        engrais = EngraisService.changer_statut(pk, data.get('statut'))
        return JsonResponse(_serialize(engrais))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)
