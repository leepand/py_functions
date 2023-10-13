def duplicate_removal(src_list):
    name_scope = set()
    dest_list = []
    for item in src_list:
        if item in name_scope:
            continue
        name_scope.add(item)
        dest_list.append(item)
    return dest_list
