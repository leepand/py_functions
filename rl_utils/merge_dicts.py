def merge_dicts(source: Dict[str, Any], destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            if isinstance(value, list):
                if key in destination:
                    destination[key].extend(value)
                else:
                    destination[key] = value
            else:
                destination[key] = value
    return destination


merge_dicts({"x": 10}, {"xx": 20})
