
#  views/utilisateur_views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from ferme.services import UtilisateurService


def _serialize(u):
    return {
        'id':          u.pk,
        'nom_complet': u.nom_complet,
        'login':       u.login,
        'role':        u.role,
        'telephone':   u.telephone,
        'actif':       u.actif,
        'is_staff':    u.is_staff,
    }


@csrf_exempt
@require_http_methods(["GET"])
def utilisateur_list(request):
    """GET /utilisateurs/ — liste avec filtres ?role=&actif="""
    role  = request.GET.get('role')
    actif = request.GET.get('actif')
    if actif is not None:
        actif = actif.lower() == 'true'
    qs = UtilisateurService.lister(role=role, actif=actif)
    return JsonResponse([_serialize(u) for u in qs], safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def utilisateur_create(request):
    """POST /utilisateurs/create/"""
    try:
        data = json.loads(request.body)
        utilisateur = UtilisateurService.creer(data)
        return JsonResponse(_serialize(utilisateur), status=201)
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def utilisateur_detail(request, pk):
    """GET /utilisateurs/<pk>/"""
    try:
        u = UtilisateurService.obtenir(pk)
        return JsonResponse(_serialize(u))
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def utilisateur_update(request, pk):
    """PUT /utilisateurs/<pk>/update/"""
    try:
        data = json.loads(request.body)
        u = UtilisateurService.modifier(pk, data)
        return JsonResponse(_serialize(u))
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def utilisateur_delete(request, pk):
    """DELETE /utilisateurs/<pk>/delete/ — soft delete"""
    try:
        result = UtilisateurService.supprimer(pk)
        return JsonResponse(result)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def utilisateur_toggle_actif(request, pk):
    """POST /utilisateurs/<pk>/toggle-actif/"""
    try:
        result = UtilisateurService.toggle_actif(pk)
        return JsonResponse(result)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def utilisateur_login(request):
    """POST /auth/login/ — authentification"""
    try:
        data     = json.loads(request.body)
        login    = data.get('login', '')
        password = data.get('password', '')
        u = UtilisateurService.authentifier(login, password)
        return JsonResponse({'message': 'Connexion réussie.', 'utilisateur': _serialize(u)})
    except (ValidationError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=401)
