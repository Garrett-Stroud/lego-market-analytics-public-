def extract_theme_name(theme_data: dict | None) -> str | None:
    if not theme_data:
        return None
    return theme_data.get("name")

def extract_subtheme_name(theme_data: dict | None, client) -> str | None:
    if not theme_data:
        return None

    parent_id = theme_data.get("parent_id")
    if not parent_id:
        return None

    parent = client.fetch_theme(parent_id)
    if not parent:
        return None

    return parent.get("name")
