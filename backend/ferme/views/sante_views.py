
#  views/sante_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import SanteService


def _serialize(s):
    return {
        'id':                  s.pk,
        'date_evenement':      str(s.date_evenement),
        'type_acte':           s.type_acte,
        'description':         s.description,
        'medicament_utilise':  s.medicament_utilise,
        'cout_ariary':         float(s.cout_ariary) if s.cout_ariary else None,
        'veterinaire':         s.veterinaire,
        'prochain_rdv':        str(s.prochain_rdv) if s.prochain_rdv else None,
        'animal': {
            'id':  s.animal.pk,
            'num': s.animal.num_identification,
        },
    }


@csrf_exempt
@require_http_methods(["GET"])
def sante_list(request):
    """GET /sante/?animal_id=&type_acte=&date_debut=&date_fin="""
    qs = SanteService.lister(
        animal_id  = request.GET.get('animal_id'),
        type_acte  = request.GET.get('type_acte'),
        date_debut = request.GET.get('date_debut'),
        date_fin   = request.GET.get('date_fin'),
    )
    return JsonResponse([_serialize(s) for s in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def sante_create(request):
    """POST /sante/create/"""
    try:
        data = json.loads(request.body)
        soin = SanteService.creer(data)
        return JsonResponse(_serialize(soin), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def sante_detail(request, pk):
    """GET /sante/<pk>/"""
    try:
        return JsonResponse(_serialize(SanteService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def sante_update(request, pk):
    """PUT /sante/<pk>/update/"""
    try:
        data = json.loads(request.body)
        soin = SanteService.modifier(pk, data)
        return JsonResponse(_serialize(soin))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def sante_delete(request, pk):
    """DELETE /sante/<pk>/delete/"""
    try:
        return JsonResponse(SanteService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def sante_rdv_a_venir(request):
    """GET /sante/rdv/?jours=30"""
    jours = int(request.GET.get('jours', 30))
    qs    = SanteService.rdv_a_venir(jours=jours)
    return JsonResponse([_serialize(s) for s in qs], safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def sante_cout_animal(request, animal_id):
    """GET /sante/cout/<animal_id>/"""
    return JsonResponse(SanteService.cout_total_par_animal(animal_id))
