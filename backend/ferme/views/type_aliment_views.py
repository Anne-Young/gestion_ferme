
#  views/type_aliment_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import TypeAlimentService


def _serialize(a):
    return {
        'id':                    a.pk,
        'nom':                   a.nom,
        'categorie':             a.categorie,
        'unite_mesure':          a.unite_mesure,
        'cout_unitaire_ariary':  float(a.cout_unitaire_ariary) if a.cout_unitaire_ariary else None,
        'origine':               a.origine,
    }


@csrf_exempt
@require_http_methods(["GET"])
def type_aliment_list(request):
    """GET /aliments/?categorie=&origine="""
    qs = TypeAlimentService.lister(
        categorie=request.GET.get('categorie'),
        origine=request.GET.get('origine'),
    )
    return JsonResponse([_serialize(a) for a in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def type_aliment_create(request):
    """POST /aliments/create/"""
    try:
        data = json.loads(request.body)
        return JsonResponse(_serialize(TypeAlimentService.creer(data)), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def type_aliment_detail(request, pk):
    """GET /aliments/<pk>/"""
    try:
        return JsonResponse(_serialize(TypeAlimentService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def type_aliment_update(request, pk):
    """PUT /aliments/<pk>/update/"""
    try:
        data = json.loads(request.body)
        return JsonResponse(_serialize(TypeAlimentService.modifier(pk, data)))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def type_aliment_delete(request, pk):
    """DELETE /aliments/<pk>/delete/"""
    try:
        return JsonResponse(TypeAlimentService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
