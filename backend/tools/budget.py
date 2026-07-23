def allocate_budget(total_budget: float, num_days: int) -> dict:
    """Splits a total trip budget into standard categories.

    Call this whenever you need a cost breakdown for a trip instead of
    guessing numbers yourself. Given the traveller's total budget and trip
    duration, returns a fixed-percentage split across standard categories
    plus a per-day estimate for daily-recurring costs.

    Args:
        total_budget: The traveller's stated total budget for the whole trip.
        num_days: The number of days in the trip.

    Returns:
        A dict with a category breakdown, a per_day_estimate for the
        recurring categories, and total_allocated as a sanity check.
    """
    if total_budget <= 0 or num_days <= 0:
        return {"error": "total_budget and num_days must be positive numbers."}

    allocation_pct = {
        "transport": 0.25,
        "accommodation": 0.25,
        "food": 0.20,
        "local_transport": 0.10,
        "activities": 0.15,
        "contingency": 0.05,
    }

    breakdown = {
        category: round(total_budget * pct)
        for category, pct in allocation_pct.items()
    }

    recurring = ["accommodation", "food", "local_transport", "activities"]
    per_day_estimate = round(sum(breakdown[c] for c in recurring) / num_days)

    return {
        "breakdown": breakdown,
        "per_day_estimate": per_day_estimate,
        "total_allocated": sum(breakdown.values()),
    }
