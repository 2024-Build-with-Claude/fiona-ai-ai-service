def list_to_or_string(items: list[str]) -> str:
    """
    Convert a list of strings to a single string with items separated by ' OR '.
    """
    return " OR ".join(f"({item})" for item in items)
