import re

import exchange_calendars as xcals
import pandas as pd


TRADING_DATE_PATTERN = re.compile(r"^T(?P<offset>[+-]\d+)?$")


def resolve_date(
        exchange: str,
        expression: str,
        base_date: str | None = None,
) -> str:
    """
    Resolve a trading-date expression to a YYYY-MM-DD date string.

    T is defined as the latest trading session on or before base_date.

    Supported expressions:
        T
        T-1
        T-20
        T+1
    """
    match = TRADING_DATE_PATTERN.fullmatch(expression)

    if match is None:
        raise ValueError(
            f"Unsupported trading-date expression: {expression}. "
            "Expected format: T, T-1, or T+1."
        )

    calendar = xcals.get_calendar(exchange)

    if base_date is None:
        base = pd.Timestamp.today().normalize()
    else:
        base = pd.Timestamp(base_date)

    sessions = calendar.sessions

    base_index = sessions.searchsorted(base, side="right") - 1

    if base_index < 0:
        raise ValueError(
            f"No trading session found on or before base_date: {base_date}"
        )

    offset_text = match.group("offset")
    offset = int(offset_text) if offset_text is not None else 0

    resolved_index = base_index + offset

    if resolved_index < 0 or resolved_index >= len(sessions):
        raise ValueError(
            f"Trading-date expression out of calendar range: "
            f"expression={expression}, base_date={base.strftime('%Y-%m-%d')}"
        )

    resolved = sessions[resolved_index]

    return resolved.strftime("%Y-%m-%d")

def is_market_closed(exchange: str, date: str) -> bool:
    """
    Return whether the given date is a market holiday.

    Args:
        exchange: Exchange calendar code (e.g. XKRX, XNYS).
        date: Date in YYYY-MM-DD format.

    Returns:
        True if the market is closed, otherwise False.
    """
    calendar = xcals.get_calendar(exchange)
    return not calendar.is_session(pd.Timestamp(date))