"""
Timestamp conversion for Microsoft Sticky Notes databases.

Modern Sticky Notes (plum.sqlite) stores CreatedAt/UpdatedAt/DeletedAt as
.NET DateTime ticks: 100-nanosecond intervals since 0001-01-01 00:00:00.
Some older builds used Windows FILETIME (same tick size, epoch 1601-01-01).
This module autodetects the epoch by magnitude and converts both directions.
"""

from datetime import datetime
from typing import Optional, Union

TICKS_PER_SECOND = 10_000_000
# Seconds between 0001-01-01 and 1970-01-01 (Unix epoch)
DOTNET_EPOCH_OFFSET_S = 62_135_596_800
# Seconds between 1601-01-01 and 1970-01-01
FILETIME_EPOCH_OFFSET_S = 11_644_473_600

# .NET ticks for dates 1900-2200 fall in ~5.99e17..6.94e17.
# FILETIME for the same range falls in ~0.94e17..1.89e17.
_DOTNET_TICKS_MIN = 5 * 10**17
_TICKS_MIN = 10**16
_UNIX_MILLIS_MIN = 10**11


def raw_to_datetime(value: Union[int, float, str, None]) -> Optional[datetime]:
    """
    Convert a raw database timestamp to a local datetime.

    Accepts .NET ticks, Windows FILETIME, Unix seconds or milliseconds,
    detected by magnitude. Returns None if the value is missing or cannot
    be interpreted.
    """
    if value is None:
        return None

    try:
        v = int(value)
    except (TypeError, ValueError):
        # Maybe it's already a formatted date string
        if isinstance(value, str):
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
                try:
                    return datetime.strptime(value[:19], fmt)
                except ValueError:
                    continue
        return None

    if v <= 0:
        return None

    if v >= _DOTNET_TICKS_MIN:
        unix_seconds = v / TICKS_PER_SECOND - DOTNET_EPOCH_OFFSET_S
    elif v >= _TICKS_MIN:
        unix_seconds = v / TICKS_PER_SECOND - FILETIME_EPOCH_OFFSET_S
    elif v >= _UNIX_MILLIS_MIN:
        unix_seconds = v / 1000.0
    else:
        unix_seconds = float(v)

    try:
        return datetime.fromtimestamp(unix_seconds)
    except (OverflowError, OSError, ValueError):
        return None


def datetime_to_ticks(dt: datetime) -> int:
    """Convert a datetime to .NET DateTime ticks (modern plum.sqlite format)."""
    return int((dt.timestamp() + DOTNET_EPOCH_OFFSET_S) * TICKS_PER_SECOND)


def now_ticks() -> int:
    """Current time as .NET DateTime ticks."""
    return datetime_to_ticks(datetime.now())


def format_timestamp(value: Union[int, float, str, None],
                     default: str = 'Unknown') -> str:
    """Format a raw database timestamp as 'YYYY-MM-DD HH:MM:SS'."""
    dt = raw_to_datetime(value)
    if dt is None:
        return default
    return dt.strftime('%Y-%m-%d %H:%M:%S')
