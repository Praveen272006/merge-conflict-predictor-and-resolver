def calculate_signals(commits, total_files, total_changes):

    ratio = total_changes / total_files if total_files else 0

    return {
        "files_changed": total_files,
        "total_changes": total_changes,
        "ratio": round(ratio, 2),
        "large_change": "YES" if total_changes > 50 else "NO",
        "multi_file": "YES" if total_files > 3 else "NO",
        "merge": "YES" if len(commits) > 1 else "NO"
    }