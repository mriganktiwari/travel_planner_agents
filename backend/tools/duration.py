"""Deterministic duration-validation tool, used by root_agent.

Plain Python — no LLM/ADK involved — so it's testable standalone and gives
a repeatable sanity check instead of letting the model judge on its own.
"""


def validate_trip_duration(num_days: int) -> dict:
    """Validates a requested trip duration.

    Call this once you've extracted a trip duration from the user's
    request, before delegating any work, to check it's a sane, usable
    number of days rather than trusting your own judgement.

    Args:
        num_days: The number of days the traveller wants to travel for.

    Returns:
        A dict with:
          - valid: True if the duration is usable as-is.
          - reason: explanation if not valid.
          - suggested_range: a sane [min, max] days range for reference.
    """
    MIN_DAYS = 1
    MAX_DAYS = 30

    if not isinstance(num_days, int) or num_days < MIN_DAYS:
        return {
            "valid": False,
            "reason": f"Duration must be at least {MIN_DAYS} day(s).",
            "suggested_range": [MIN_DAYS, MAX_DAYS],
        }
    if num_days > MAX_DAYS:
        return {
            "valid": False,
            "reason": f"{num_days} days is unusually long for this MVP planner.",
            "suggested_range": [MIN_DAYS, MAX_DAYS],
        }
    return {"valid": True, "reason": "", "suggested_range": [MIN_DAYS, MAX_DAYS]}
