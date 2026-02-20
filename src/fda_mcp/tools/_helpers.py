"""Shared helpers for MCP tool handlers."""


def clamp_limit(limit: int, max_limit: int) -> tuple[int, str | None]:
    """Clamp limit to max_limit, returning a note if it was reduced.

    Returns:
        (clamped_limit, note) — note is None if limit was within bounds,
        otherwise a human-readable string explaining the reduction.
    """
    if limit > max_limit:
        return max_limit, (
            f"[Note: limit was reduced from {limit} to {max_limit} "
            f"(maximum allowed).]"
        )
    return limit, None
