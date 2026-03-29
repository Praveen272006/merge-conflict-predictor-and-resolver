def generate_resolution(head_code, incoming_code):
    """
    AI Merge Conflict Resolution Generator
    """

    if not head_code:
        return {
            "solution": incoming_code,
            "reason": "Only incoming change exists"
        }

    if not incoming_code:
        return {
            "solution": head_code,
            "reason": "Only HEAD version exists"
        }

    # Prefer meaningful variable names
    if "qty" in head_code and "quantity" in incoming_code:
        return {
            "solution": incoming_code,
            "reason": "More descriptive variable used"
        }

    # Prefer longer logic
    if len(incoming_code) > len(head_code):
        return {
            "solution": incoming_code,
            "reason": "Incoming code more complete"
        }

    return {
        "solution": head_code,
        "reason": "HEAD version retained"
    }