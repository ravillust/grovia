"""
Timezone utilities untuk handling timezone user
"""
from datetime import timezone, timedelta
from typing import Optional, Union
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

# Try to import zoneinfo, fallback to pytz if not available
try:
    from zoneinfo import ZoneInfo
    USE_ZONEINFO = True
except ImportError:
    try:
        import pytz
        USE_ZONEINFO = False
    except ImportError:
        USE_ZONEINFO = None
        logger.warning("Neither zoneinfo nor pytz available, using manual timezone offsets")

def get_timezone(tz_name: str) -> Union[timezone, 'ZoneInfo', 'pytz.timezone']:
    """
    Get timezone object based on available library
    """
    if USE_ZONEINFO:
        try:
            return ZoneInfo(tz_name)
        except Exception as e:
            logger.debug(f"ZoneInfo failed for {tz_name}: {e}")
            return None
    elif USE_ZONEINFO is False:
        try:
            return pytz.timezone(tz_name)
        except Exception as e:
            logger.debug(f"pytz failed for {tz_name}: {e}")
            return None
    return None

def resolve_user_timezone(request: Optional[Request], user) -> Union[timezone, 'ZoneInfo', 'pytz.timezone']:
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
            tz = get_timezone(tz_header)
            if tz:
                return tz
            logger.warning(f"Invalid timezone from header: {tz_header}")
    
    # 2. Cek user profile timezone (jika user punya setting timezone)
    if user and hasattr(user, "timezone") and user.timezone:
        tz = get_timezone(user.timezone)
        if tz:
            return tz
        logger.warning(f"Invalid timezone from user profile: {user.timezone}")
    
    # 3. Default timezone: Coba beberapa variasi untuk WITA (UTC+8)
    timezone_options = [
        "Asia/Makassar",      # WITA - Kalimantan, Sulawesi
        "Asia/Singapore",     # UTC+8 (sama dengan WITA)
        "Asia/Kuala_Lumpur",  # UTC+8 (sama dengan WITA)
        "Asia/Manila",        # UTC+8 (sama dengan WITA)
    ]
    
    for tz_name in timezone_options:
        tz = get_timezone(tz_name)
        if tz:
            logger.info(f"Using timezone: {tz_name}")
            return tz
    
    # 4. Fallback: Gunakan timezone dengan offset manual UTC+8
    logger.info("Using manual UTC+8 offset (WITA)")
    return timezone(timedelta(hours=8))