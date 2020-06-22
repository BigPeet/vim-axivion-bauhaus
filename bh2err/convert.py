import os.path

STYLE_VIOLATION_HEADERS = ["Id", "State", "Suppressed", "Error Number",
                           "Message", "Entity", "Path", "Line", "Provider", "Severity",
                           "Justification", "Tags"]
CSV_SEPARATOR = ";"


def convert_file(path, version):

    if not os.path.isfile(path):
        return []

    content = ""

    with open(path, "r") as f:
        content = f.read()

    if len(content) > 0:
        return convert_text(content, version)
    return []


def convert_text(content, version):
    content = content.strip()
    new_line_idx = content.find("\n")

    if new_line_idx == -1:
        return []

    output = []
    headers = content[:new_line_idx].replace("\"", "").split(CSV_SEPARATOR)
    if (new_line_idx + 1) < len(content):
        entries = __split_into_entries(content[new_line_idx + 1:], len(headers))
        if headers == STYLE_VIOLATION_HEADERS:
            output = __convert_style_violations(entries)

    return output


def __split_into_entries(content, length):
    entries = []
    entry_start = 0
    while entry_start < len(content):
        start = entry_start
        for _ in range(length - 1):
            start = content.find(CSV_SEPARATOR, start)
            if start == -1:
                return []  # not well-formed CSV
            else:
                start += 1
        if start != -1:
            start = content.find("\n", start)
            if start != -1:
                entries.append(content[entry_start:start])
            else:
                entries.append(content[entry_start:])
        else:
            return []  # not well-formed CSV
        if start != -1:
            entry_start = start + 1
        else:
            entry_start = len(content)
    return entries


def __tokenize_entry(entry):
    tokens = []
    it = 0
    entry_start = 0

    while it < len(entry):
        sep = entry.find(CSV_SEPARATOR, it)
        if sep == -1:
            # last token
            tokens.append(entry[entry_start:])
            return tokens

        # might still lead to problems, if there are multiple nested ""
        if entry.count("\"", entry_start, sep) % 2 == 0:
            token = entry[entry_start:sep]
            tokens.append(token)
            entry_start = sep + 1
        it = sep + 1
    return []


def __get_token(tokens, index):
    if index < 0 or index >= len(tokens):
        return ""
    return tokens[index].strip()[1:-1]


def __convert_style_violations(entries):
    violations = []
    for entry in entries:
        tokens = __tokenize_entry(entry)

        filename = __get_token(tokens, STYLE_VIOLATION_HEADERS.index("Path"))
        line_num = __get_token(tokens, STYLE_VIOLATION_HEADERS.index("Line"))
        message = __get_token(tokens, STYLE_VIOLATION_HEADERS.index("Message"))
        severity = __get_token(tokens, STYLE_VIOLATION_HEADERS.index("Severity"))
        error_num = __get_token(tokens, STYLE_VIOLATION_HEADERS.index("Error Number"))

        if line_num.isdigit():
            line_num = max(0, int(line_num))
        else:
            line_num = 0

        text = ""
        if error_num and message:
            text = error_num + ": " + message
        elif error_num:
            text = error_num
        elif message:
            text = message

        violation = dict()
        violation["filename"] = filename
        violation["lnum"] = line_num
        violation["text"] = text
        if severity == "warning" or severity == "advisory":
            violation["type"] = "W"
        elif severity:
            violation["type"] = "E"
        else:
            violation["type"] = ""
        violation["nr"] = error_num

        violations.append(violation)
    return violations
