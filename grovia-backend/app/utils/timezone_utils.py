"""
Timezone utilities untuk handling timezone user
"""
from datetime import timezone, timedelta
from zoneinfo import ZoneInfo
from typing import Optional
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

def resolve_user_timezone(request: Optional[Request], user) -> ZoneInfo:
    """
    Resolve timezone user berdasarkan:
    1. Header X-Timezone dari request
    2. User profile timezone
    3. Default: UTC+8 (WITA - Samarinda, Kalimantan Timur)
    """
    
    # 1. Cek header request (jika frontend mengirim timezone)
    if request:
        tz_header = request.headers.get("X-Timezone")
        if tz_header:
            try:
                return ZoneInfo(tz_header)
            except Exception as e:
                logger.warning(f"Invalid timezone from header: {tz_header}, error: {e}")
    
    # 2. Cek user profile timezone (jika user punya setting timezone)
    if user and hasattr(user, "timezone") and user.timezone:
        try:
            return ZoneInfo(user.timezone)
        except Exception as e:
            logger.warning(f"Invalid timezone from user profile: {user.timezone}, error: {e}")
    
    # 3. Default timezone: Coba beberapa variasi untuk WITA (UTC+8)
    timezone_options = [
        "Asia/Makassar",      # WITA - Kalimantan, Sulawesi
        "Asia/Singapore",     # UTC+8 (sama dengan WITA)
        "Asia/Kuala_Lumpur",  # UTC+8 (sama dengan WITA)
        "Asia/Manila",        # UTC+8 (sama dengan WITA)
    ]
    
    for tz_name in timezone_options:
        try:
            return ZoneInfo(tz_name)
        except Exception:
            continue
    
    # 4. Fallback: Gunakan timezone dengan offset manual UTC+8
    logger.warning("All timezone options failed, using manual UTC+8 offset")
    return timezone(timedelta(hours=8))