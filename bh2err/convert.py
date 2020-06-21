STYLE_VIOLATION_HEADERS = ["Id", "State", "Suppressed", "Error Number",
        "Message", "Entity", "Path", "Line", "Provider", "Severity",
        "Justification", "Tags"]
CSV_SEPARATOR = ";"


def convert_file(path, version):
    content = ""
    with open(path, "r") as f:
        content = f.read()

    if len(content) > 0:
        return convert_text(content, version)
    return []

def convert_text(content, version):
    output = []
    content = content.strip()
    headers = content[:content.index("\n")].replace("\"", "").split(CSV_SEPARATOR)
    entries = split_into_entries(content[content.index("\n") + 1:], len(headers))
    if headers == STYLE_VIOLATION_HEADERS:
        output = convert_style_violations(entries)

    return output

def split_into_entries(content, length):
    entries = []
    entry_start = 0
    while entry_start < len(content):
        start = entry_start
        for _ in range(length - 1):
            start = content.find(CSV_SEPARATOR, start)
            if start == -1:
                return [] # not well-formed CSV
            else:
                start += 1
        if start != -1:
            start = content.find("\n", start)
            if start != -1:
                entries.append(content[entry_start:start])
            else:
                entries.append(content[entry_start:])
        else:
            return [] # not well-formed CSV
        if start != -1:
            entry_start = start + 1
        else:
            entry_start = len(content)
    return entries

def tokenize_entry(entry):
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


def convert_style_violations(entries):
    violations = []
    for entry in entries:
        tokens = tokenize_entry(entry)
        # tokens = entry.split(CSV_SEPARATOR)
        violation = dict()
        violation["filename"] = tokens[STYLE_VIOLATION_HEADERS.index("Path")].strip()[1:-1]
        violation["lnum"] = int(tokens[STYLE_VIOLATION_HEADERS.index("Line")].strip()[1:-1])
        violation["text"] = tokens[STYLE_VIOLATION_HEADERS.index("Message")].strip()[1:-1]
        severity = tokens[STYLE_VIOLATION_HEADERS.index("Severity")].strip()[1:-1]
        if severity == "warning" or severity == "advisory":
            violation["type"] = "W"
        else:
            violation["type"] = "E"
        violation["nr"] = tokens[STYLE_VIOLATION_HEADERS.index("Error Number")].strip()[1:-1]
        violations.append(violation)
    return violations
