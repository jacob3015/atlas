import exchange_calendars as xcals
import pandas as pd


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