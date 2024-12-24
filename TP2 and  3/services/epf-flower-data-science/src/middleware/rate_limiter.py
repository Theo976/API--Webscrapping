from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

def rate_limit_key(request: Request):
    """Generate rate limit key based on IP and user"""
    try:
        token = request.headers.get('Authorization')
        if token:
            from src.auth.firebase_auth import verify_token
            user_id = verify_token(token).get('uid')
            return f"{get_remote_address(request)}:{user_id}"
    except:
        pass
    return get_remote_address(request)