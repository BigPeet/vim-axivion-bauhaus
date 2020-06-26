import os.path
import csv

STYLE_VIOLATION_HEADERS = ["Id", "State", "Suppressed", "Error Number",
                           "Message", "Entity", "Path", "Line", "Provider", "Severity",
                           "Justification", "Tags"]
CSV_SEPARATOR = ";"

def convert_file(path, version):
    if not os.path.isfile(path):
        return []

    content = ""
    with open(path, "r", newline="") as f:
        content = f.read()

    if len(content) > 0:
        return convert_text(content, version)
    return []

def convert_text(content, version):
    output = []
    if content:
        reader = csv.reader(content.strip().split("\n"), delimiter=";", )

        entries = []
        for line_num, row in enumerate(reader):
            if line_num > 0:
                entries.append(row)
            else:
                headers = row

        if headers == STYLE_VIOLATION_HEADERS:
            output = __convert_style_violations(entries)

    return output

def __convert_style_violations(entries):
    violations = []
    for token in entries:
        filename = token[STYLE_VIOLATION_HEADERS.index("Path")]
        line_num = token[STYLE_VIOLATION_HEADERS.index("Line")]
        message = token[STYLE_VIOLATION_HEADERS.index("Message")]
        severity = token[STYLE_VIOLATION_HEADERS.index("Severity")]
        error_num = token[STYLE_VIOLATION_HEADERS.index("Error Number")]

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
