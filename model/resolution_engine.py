import re


# =========================
# TOKENIZER
# =========================
def tokenize(line):
    return re.findall(r'\w+', line)


# =========================
# VARIABLE MAPPING
# =========================
def detect_variable_mapping(a, b):
    tokens_a = tokenize(a)
    tokens_b = tokenize(b)

    mapping = {}

    for x, y in zip(tokens_a, tokens_b):
        if x != y:
            mapping[x] = y

    return mapping


# =========================
# APPLY MAPPING
# =========================
def apply_mapping(line, mapping):
    for k, v in mapping.items():
        line = re.sub(rf"\b{k}\b", v, line)
    return line


# =========================
# SMART MERGE (LINE)
# =========================
def smart_merge(line_a, line_b):

    a = line_a.strip()
    b = line_b.strip()

    if a == b:
        return a

    mapping = detect_variable_mapping(a, b)

    if len(a) < len(b):
        return apply_mapping(a, mapping)
    else:
        return apply_mapping(b, mapping)


# =========================
# BLOCK MERGE
# =========================
def merge_blocks(old_block, new_block):

    merged_lines = []
    max_len = max(len(old_block), len(new_block))

    for i in range(max_len):

        old_line = old_block[i] if i < len(old_block) else ""
        new_line = new_block[i] if i < len(new_block) else ""

        if old_line and new_line:
            merged_lines.append(smart_merge(old_line, new_line))
        elif new_line:
            merged_lines.append(new_line)
        else:
            merged_lines.append(old_line)

    return "\n".join(merged_lines)


# =========================
# MAIN ENGINE
# =========================
def generate_resolution(commit_data):

    resolutions = []
    files = commit_data.get("files", [])

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch")

        if not patch:
            continue

        lines = patch.split("\n")

        line_number = 0
        old_block = []
        new_block = []
        block_start = 0

        # 🔥 FINAL MERGED RESULT FOR FILE
        final_merged_lines = []

        for line in lines:

            # HUNK HEADER
            if line.startswith("@@"):
                parts = line.split(" ")
                new_info = parts[2]
                line_number = int(new_info.split(",")[0].replace("+", ""))

                old_block = []
                new_block = []
                continue

            # REMOVED
            if line.startswith("-") and not line.startswith("---"):
                if not old_block:
                    block_start = line_number
                old_block.append(line[1:].strip())

            # ADDED
            elif line.startswith("+") and not line.startswith("+++"):
                if not new_block:
                    block_start = line_number
                new_block.append(line[1:].strip())

            else:
                # PROCESS BLOCK
                if old_block or new_block:

                    merged = merge_blocks(old_block, new_block)
                    final_merged_lines.append(merged)

                    old_block = []
                    new_block = []

                line_number += 1

        # LAST BLOCK
        if old_block or new_block:
            merged = merge_blocks(old_block, new_block)
            final_merged_lines.append(merged)

        # 🔥 ONLY ONE OUTPUT PER FILE
        if final_merged_lines:

            final_code = "\n".join(final_merged_lines)

            resolutions.append({
                "file": filename,
                "line": 1,
                "type": "MERGED",
                "issue": "Conflicting logic",
                "code": final_code,
                "fix": final_code,
                "explanation": "AI merged all conflicting changes into a single optimized solution"
            })

    return resolutions