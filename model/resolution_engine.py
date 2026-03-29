def generate_resolution(old_code, new_code):

    old_code = old_code.strip()
    new_code = new_code.strip()

    # Case 1: variable naming improvement
    if old_code.replace("qty", "quantity") == new_code:
        return new_code

    # Case 2: whitespace only change
    if old_code.replace(" ", "") == new_code.replace(" ", ""):
        return new_code

    # Case 3: prefer longer (more descriptive)
    if len(new_code) > len(old_code):
        return new_code

    return old_code