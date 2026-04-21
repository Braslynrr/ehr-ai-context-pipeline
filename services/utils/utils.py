

def dict_diff(old: dict, new: dict):
    diff = {}

    keys = set(old.keys()) | set(new.keys())

    for key in keys:
        old_val = old.get(key)
        new_val = new.get(key)

        if old_val != new_val:
            diff[key] = {
                "old": old_val,
                "new": new_val
            }

    return diff


def format_changes(diff):
    return ", ".join(
        f"{k}: {v['old']} → {v['new']}"
        for k, v in diff.items()
    )