
#  views/stock_aliment_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import StockAlimentService


def _serialize(s):
    return {
        'id':                   s.pk,
        'type_aliment': {
            'id':  s.type_aliment.pk,
            'nom': s.type_aliment.nom,
        },
        'quantite_disponible':  float(s.quantite_disponible),
        'seuil_alerte':         float(s.seuil_alerte) if s.seuil_alerte else None,
        'en_alerte':            s.en_alerte,
        'date_maj':             s.date_maj.isoformat(),
    }


@csrf_exempt
@require_http_methods(["GET"])
def stock_aliment_list(request):
    """GET /stocks/aliments/?en_alerte=true"""
    en_alerte = request.GET.get('en_alerte', '').lower() == 'true'
    result = StockAlimentService.lister(en_alerte_only=en_alerte)
    return JsonResponse([_serialize(s) for s in result], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def stock_aliment_create(request):
    """POST /stocks/aliments/create/"""
    try:
        data = json.loads(request.body)
        return JsonResponse(_serialize(StockAlimentService.creer(data)), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def stock_aliment_detail(request, pk):
    """GET /stocks/aliments/<pk>/"""
    try:
        return JsonResponse(_serialize(StockAlimentService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def stock_aliment_update(request, pk):
    """PUT /stocks/aliments/<pk>/update/"""
    try:
        data = json.loads(request.body)
        return JsonResponse(_serialize(StockAlimentService.modifier(pk, data)))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def stock_aliment_delete(request, pk):
    """DELETE/stocks/aliments/<pk>/delete/"""
    try:
        return JsonResponse(StockAlimentService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def stock_aliment_ajouter(request, pk):
    """POST /stocks/aliments/<pk>/ajouter/ — body: {"quantite": 50}"""
    try:
        data = json.loads(request.body)
        q    = float(data.get('quantite', 0))
        return JsonResponse(_serialize(StockAlimentService.ajouter_stock(pk, q)))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def stock_aliment_retirer(request, pk):
    """POST /stocks/aliments/<pk>/retirer/ — body: {"quantite": 10}"""
    try:
        data = json.loads(request.body)
        q    = float(data.get('quantite', 0))
        return JsonResponse(_serialize(StockAlimentService.retirer_stock(pk, q)))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)
