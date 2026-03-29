def calculate_signals(commits, total_files, total_changes):

    files_changed = total_files
    total_changes_val = total_changes

    ratio = total_changes_val / files_changed if files_changed else 0

    large_change = "YES" if total_changes_val > 50 else "NO"
    multi_file = "YES" if files_changed > 3 else "NO"
    merge = "YES" if len(commits) > 1 else "NO"

    return {
        "files_changed": files_changed,
        "total_changes": total_changes_val,
        "ratio": round(ratio, 2),
        "large_change": large_change,
        "multi_file": multi_file,
        "merge": merge
    }