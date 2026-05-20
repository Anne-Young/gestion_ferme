import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
 
from ferme.models import Utilisateur

 
 
def _user_data(user):
    """Sérialise uniquement les infos utiles au frontend."""
    return {
        'id':          user.pk,
        'nom_complet': user.nom_complet,
        'login':       user.login,
        'role':        user.role,
    }
 
 
# ── POST /api/auth/login/ ────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """
    Body attendu :
        { "login": "rakoto.jean", "password": "monmotdepasse" }
 
    Réponse OK :
        { "access": "...", "refresh": "...", "utilisateur": {...} }
    """
    try:
        data     = json.loads(request.body)
        login    = data.get('login', '').strip()
        password = data.get('password', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Corps JSON invalide.'}, status=400)
 
    if not login or not password:
        return JsonResponse(
            {'error': 'Le login et le mot de passe sont obligatoires.'},
            status=400
        )
 
    # Django authenticate utilise USERNAME_FIELD = 'login'
    # donc on passe username=login
    user = authenticate(request, username=login, password=password)
 
    if user is None:
        return JsonResponse(
            {'error': 'Identifiant ou mot de passe incorrect.'},
            status=401
        )
 
    if not user.actif:
        return JsonResponse(
            {'error': 'Ce compte a été désactivé. Contactez votre administrateur.'},
            status=403
        )
 
    # Génération des tokens JWT
    refresh = RefreshToken.for_user(user)
 
    return JsonResponse({
        'access':       str(refresh.access_token),
        'refresh':      str(refresh),
        'utilisateur':  _user_data(user),
    }, status=200)
 
 
# ── POST /api/auth/refresh/ ──────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def refresh_view(request):
    """
    Body : { "refresh": "<refresh_token>" }
    Retourne un nouvel access token sans se reconnecter.
    """
    try:
        data  = json.loads(request.body)
        token = RefreshToken(data.get('refresh', ''))
        return JsonResponse({'access': str(token.access_token)}, status=200)
    except TokenError:
        return JsonResponse({'error': 'Token invalide ou expiré.'}, status=401)
    except Exception:
        return JsonResponse({'error': 'Erreur serveur.'}, status=500)
 
 
# ── POST /api/auth/logout/ ───────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """
    Body : { "refresh": "<refresh_token>" }
    Blackliste le token (nécessite rest_framework_simplejwt.token_blacklist).
    """
    try:
        data    = json.loads(request.body)
        refresh = RefreshToken(data.get('refresh', ''))
        refresh.blacklist()
        return JsonResponse({'message': 'Déconnexion réussie.'}, status=200)
    except TokenError:
        # Token déjà expiré ou invalide — on considère quand même déconnecté
        return JsonResponse({'message': 'Déconnecté.'}, status=200)
    except Exception:
        return JsonResponse({'error': 'Erreur lors de la déconnexion.'}, status=500)
 
 
# ── GET /api/auth/me/
@csrf_exempt
@require_http_methods(["GET"])
def me_view(request):
    """
    Header : Authorization: Bearer <access_token>
    Retourne les infos de l'utilisateur actuellement connecté.
    """
    try:
        jwt_auth      = JWTAuthentication()
        user, _token  = jwt_auth.authenticate(request)
        return JsonResponse(_user_data(user), status=200)
    except Exception:
        return JsonResponse({'error': 'Non authentifié.'}, status=401)
 