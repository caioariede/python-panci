def listify(string_or_list):
    """Takes a string or a list and converts strings to one item lists"""

    if not isinstance(string_or_list, list):
        return [string_or_list]

    return string_or_list
