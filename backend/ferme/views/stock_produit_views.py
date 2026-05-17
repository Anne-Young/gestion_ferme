
#  views/stock_produit_views.py


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import StockProduitService


def _serialize(s):
    return {
        'id':                   s.pk,
        'type_produit':         s.type_produit,
        'quantite_disponible':  float(s.quantite_disponible),
        'unite':                s.unite,
        'seuil_alerte':         float(s.seuil_alerte) if s.seuil_alerte else None,
        'en_alerte':            s.en_alerte,
        'date_maj':             s.date_maj.isoformat(),
    }


@csrf_exempt
@require_http_methods(["GET"])
def stock_produit_list(request):
    """GET /stocks/produits/?en_alerte=true"""
    en_alerte = request.GET.get('en_alerte', '').lower() == 'true'
    result = StockProduitService.lister(en_alerte_only=en_alerte)
    return JsonResponse([_serialize(s) for s in result], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def stock_produit_create(request):
    """POST /stocks/produits/create/"""
    try:
        data = json.loads(request.body)
        return JsonResponse(_serialize(StockProduitService.creer(data)), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def stock_produit_detail(request, pk):
    """GET/stocks/produits/<pk>/"""
    try:
        return JsonResponse(_serialize(StockProduitService.obtenir(pk)))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def stock_produit_update(request, pk):
    """PUT /stocks/produits/<pk>/update/"""
    try:
        data = json.loads(request.body)
        return JsonResponse(_serialize(StockProduitService.modifier(pk, data)))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def stock_produit_delete(request, pk):
    """DELETE /stocks/produits/<pk>/delete/"""
    try:
        return JsonResponse(StockProduitService.supprimer(pk))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def stock_produit_ajouter(request):
    """POST /stocks/produits/ajouter/ — body: {"type_produit": "lait", "quantite": 50}"""
    try:
        data = json.loads(request.body)
        tp   = data.get('type_produit')
        q    = float(data.get('quantite', 0))
        return JsonResponse(_serialize(StockProduitService.ajouter_stock(tp, q)))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def stock_produit_retirer(request):
    """POST /stocks/produits/retirer/ — body: {"type_produit": "lait", "quantite": 20}"""
    try:
        data = json.loads(request.body)
        tp   = data.get('type_produit')
        q    = float(data.get('quantite', 0))
        return JsonResponse(_serialize(StockProduitService.retirer_stock(tp, q)))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)
