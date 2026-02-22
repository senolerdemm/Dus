"""
Infrastructure — Supabase Auth Client
=======================================
Supabase üzerinden kullanıcı kimlik doğrulama.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

_supabase: Client | None = None


def get_supabase() -> Client:
    """Supabase client singleton."""
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL ve SUPABASE_KEY ortam değişkenleri gerekli")
        _supabase = create_client(url, key)
    return _supabase


def supabase_register(email: str, password: str, full_name: str) -> dict:
    """
    Supabase Auth ile kayıt.
    Returns: { "user_id": str, "access_token": str, "refresh_token": str }
    """
    sb = get_supabase()
    response = sb.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {"full_name": full_name}
        }
    })

    user = response.user
    session = response.session

    if not user:
        raise ValueError("Kayıt başarısız")

    return {
        "user_id": user.id,
        "email": user.email,
        "full_name": full_name,
        "access_token": session.access_token if session else "",
        "refresh_token": session.refresh_token if session else "",
    }


def supabase_login(email: str, password: str) -> dict:
    """
    Supabase Auth ile giriş.
    Returns: { "user_id": str, "access_token": str, "refresh_token": str }
    """
    sb = get_supabase()
    response = sb.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    user = response.user
    session = response.session

    if not user or not session:
        raise ValueError("Giriş başarısız — email veya şifre hatalı")

    return {
        "user_id": user.id,
        "email": user.email,
        "full_name": user.user_metadata.get("full_name", ""),
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
    }


def supabase_get_user(access_token: str) -> dict | None:
    """
    Supabase JWT token'ını doğrulayıp user bilgisini döner.
    Returns: { "user_id": str, "email": str, "full_name": str } veya None
    """
    sb = get_supabase()
    try:
        response = sb.auth.get_user(access_token)
        user = response.user
        if not user:
            return None
        return {
            "user_id": user.id,
            "email": user.email or "",
            "full_name": user.user_metadata.get("full_name", ""),
        }
    except Exception:
        return None
