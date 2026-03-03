# auto_resolver/resolver.py

def has_conflict_markers(text: str) -> bool:
    """
    Detects Git conflict markers in text.
    """
    return "<<<<<<<" in text and ">>>>>>>" in text


def remove_trailing_whitespace(text: str) -> tuple[str, bool]:
    """
    Removes trailing whitespace from each line.
    Returns cleaned text and whether any change occurred.
    """
    original = text
    lines = text.split("\n")
    cleaned_lines = [line.rstrip() for line in lines]
    cleaned_text = "\n".join(cleaned_lines)

    changed = cleaned_text != original
    return cleaned_text, changed


def resolve_simple_conflict(text: str) -> tuple[str, bool]:
    """
    Resolves very simple Git conflicts where the difference
    is only whitespace.

    Example:

    <<<<<<< HEAD
    print("hello")
    =======
    print("hello")
    >>>>>>> branch

    It keeps one version and removes markers.
    """

    if not has_conflict_markers(text):
        return text, False

    lines = text.split("\n")
    resolved_lines = []
    in_conflict = False
    keep_buffer = []

    for line in lines:
        if line.startswith("<<<<<<<"):
            in_conflict = True
            keep_buffer = []
            continue

        elif line.startswith("=======") and in_conflict:
            continue

        elif line.startswith(">>>>>>>") and in_conflict:
            # keep first version only
            resolved_lines.extend(keep_buffer)
            in_conflict = False
            continue

        if in_conflict:
            keep_buffer.append(line)
        else:
            resolved_lines.append(line)

    resolved_text = "\n".join(resolved_lines)
    return resolved_text, True


def resolve_whitespace(text: str) -> dict:
    """
    Main auto-resolution function.

    Steps:
    1. Remove trailing whitespace
    2. Attempt simple conflict resolution

    Returns structured result.
    """

    result = {
        "original": text,
        "cleaned": text,
        "whitespace_fixed": False,
        "conflict_fixed": False,
        "changed": False
    }

    # Step 1: Remove trailing whitespace
    cleaned_text, whitespace_changed = remove_trailing_whitespace(text)

    result["cleaned"] = cleaned_text
    result["whitespace_fixed"] = whitespace_changed

    # Step 2: Resolve simple conflict markers
    if has_conflict_markers(cleaned_text):
        resolved_text, conflict_fixed = resolve_simple_conflict(cleaned_text)
        result["cleaned"] = resolved_text
        result["conflict_fixed"] = conflict_fixed

    result["changed"] = (
        result["whitespace_fixed"] or result["conflict_fixed"]
    )

    return result