import time
from fastapi.testclient import TestClient
import redis
import jwt

from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM


def test_blacklist_on_logout(
    client: TestClient, refresh_token: str, redis_client: redis.Redis
):
    client.cookies.set("refresh_token", refresh_token)
    
    response = client.post("/auth/logout")
    
    assert response.status_code == 204
    
    assert client.cookies.get("refresh_token") is None
    
    token_payload = jwt.decode(
        refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
    )
    token_jti = str(token_payload.get("id"))
    
    assert redis_client.exists(f"token:blacklist:{token_jti}") == 1


def test_refresh_with_blacklisted_token(
    client: TestClient, refresh_token: str, redis_client: redis.Redis
):
    token_payload = jwt.decode(
        refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
    )
    token_jti = str(token_payload.get("id"))
    
    token_exp = token_payload.get("exp")
    current_time = int(time.time())
    ttl = token_exp - current_time
    
    redis_client.setex(f"token:blacklist:{token_jti}", ttl, "1")
    
    response = client.post(
        "/auth/refresh", 
        cookies={"refresh_token": refresh_token}
    )
    
    assert response.status_code == 401


def test_access_with_blacklisted_token(
    client: TestClient, access_token: str, redis_client: redis.Redis
):
    token_payload = jwt.decode(
        access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
    )
    token_jti = str(token_payload.get("id"))
    
    token_exp = token_payload.get("exp")
    current_time = int(time.time())
    ttl = token_exp - current_time
    
    redis_client.setex(f"token:blacklist:{token_jti}", ttl, "1")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", headers=headers)
    
    assert response.status_code == 401


def test_logout_all_sessions(
    client: TestClient,
    refresh_token: str,
    access_token: str,
    add_user,
    redis_client: redis.Redis
):
    client.cookies.set("refresh_token", refresh_token)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/auth/logout-all", headers=headers)
    
    assert response.status_code == 204
    
    user_id = add_user.id
    assert redis_client.exists(f"user:tokens:blacklist:{user_id}") == 1
    
    refresh_response = client.post(
        "/auth/refresh", 
        cookies={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 401
    
    access_response = client.get("/users/me", headers=headers)
    assert access_response.status_code == 401 