# auto_resolver/resolver.py

def resolve_whitespace(conflict_text):
    """
    Removes whitespace differences from conflicts.
    Phase-1 auto resolution.
    """

    lines = conflict_text.split("\n")
    cleaned = [line.strip() for line in lines]

    return "\n".join(cleaned)