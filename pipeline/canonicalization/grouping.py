from collections import defaultdict

def group_by_set_number(items):
    groups = defaultdict(list)
    for item in items:
        if item.set_number:
            groups[item.set_number].append(item)
    return groups
