from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException

limiter = Limiter(key_func=get_remote_address)

def rate_limit_key(request: Request):
    """Génère une clé unique pour le rate limiting basée sur l'IP et l'utilisateur"""
    try:
        token = request.headers.get('Authorization')
        if token:
            # Si l'utilisateur est authentifié, utiliser son ID
            from src.auth.firebase_auth import verify_token
            user_id = verify_token(token).get('uid')
            return f"{get_remote_address(request)}:{user_id}"
    except:
        pass
    # Sinon, utiliser uniquement l'IP
    return get_remote_address(request)