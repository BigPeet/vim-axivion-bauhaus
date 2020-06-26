import os.path
import csv

STYLE_VIOLATION_HEADERS = ["Id", "State", "Suppressed", "Error Number",
                           "Message", "Entity", "Path", "Line", "Provider", "Severity",
                           "Justification", "Tags"]
ARCHITECTURE_VIOLATION_HEADERS = ["Id", "State", "Suppressed", "Violation Type", "Architecture Source",
                                  "Architecture Source Linkname", "Architecture Source Type", "Architecture Target",
                                  "Architecture Target Linkname", "Architecture Target Type", "Source Entity",
                                  "Source Linkname", "Source Entity Type", "Source Path", "Source Line",
                                  "Dependency Type", "Target Entity", "Target Linkname", "Target Entity Type",
                                  "Target Path", "Target Line", "Justification", "Tags"]
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
        if headers == ARCHITECTURE_VIOLATION_HEADERS:
            output = __convert_architecture_violations(entries)

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


def __convert_architecture_violations(entries):
    violations = []
    for token in entries:
        filename = token[ARCHITECTURE_VIOLATION_HEADERS.index("Source Path")]
        line_num = token[ARCHITECTURE_VIOLATION_HEADERS.index("Source Line")]
        source_link = token[ARCHITECTURE_VIOLATION_HEADERS.index("Source Linkname")]
        target_link = token[ARCHITECTURE_VIOLATION_HEADERS.index("Target Linkname")]
        violation_type = token[ARCHITECTURE_VIOLATION_HEADERS.index("Violation Type")]

        if line_num.isdigit():
            line_num = max(0, int(line_num))
        else:
            line_num = 0

        text = ""
        if source_link and target_link:
            text = source_link + " -> " + target_link
        elif source_link:
            text = source_link

        violation = dict()
        violation["filename"] = filename
        violation["lnum"] = line_num
        violation["text"] = text
        if violation_type == "Divergence":
            violation["type"] = "E"
        elif violation_type:
            violation["type"] = "W"
        else:
            violation["type"] = ""

        violations.append(violation)
    return violations
