def preprocessing_filter_spec(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        # Remove all but DRF API endpoints
        if "/datatables/" not in path:
            filtered.append((path, path_regex, method, callback))
    return filtered
