
FILTER_TYPES = {
    "error": "Error Number",  # for SVs
    "violation": "Violation Type",  # for AVs
    "metric": "Metric",  # for MV
    "clone": "Clone Type",  # for CL
    "path": "Path",
    "severity": "Severity",
    "message": "Message",
}


def parse_mode(mode):
    contains_op = None
    mode_op = None
    combine_op = None
    if "!" in mode:
        def contains_op(header, pattern): return pattern != header
    else:
        def contains_op(header, pattern): return header.find(pattern) == -1
    if "-" in mode:
        def mode_op(header, pattern): return not contains_op(header, pattern)
        def combine_op(ls): return any(ls)
    else:
        def mode_op(header, pattern): return contains_op(header, pattern)
        def combine_op(ls): return all(ls)

    return mode_op, combine_op


def parse_filter(input_filter):
    # filter: type:mode:pattern1[;pattern2;...]
    parsed = None
    tokens = input_filter.split(":")

    if len(tokens) > 2:
        filter_type = tokens[0]
        if filter_type in FILTER_TYPES.keys():
            header = FILTER_TYPES[filter_type]
        else:
            header = filter_type
        mode = tokens[1]
        mode_op, combine_op = parse_mode(mode)
        patterns = tokens[2].split(";")
        def parsed(row, headers):
            return combine_op([mode_op(row[headers.index(header)], pattern) for pattern in patterns])

    return parsed


def parse_filters(input_filters):
    parsed_filters = []
    for f in input_filters:
        parsed_f = parse_filter(f)
        if parsed_f:
            parsed_filters.append(parsed_f)
    return parsed_filters
