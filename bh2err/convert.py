import os.path
import csv

REQ_STYLE_VIOLATION_HEADERS = ["Error Number", "Message", "Path", "Line", "Severity"]
REQ_ARCHITECTURE_VIOLATION_HEADERS = ["Violation Type", "Source Path", "Source Line",
                                      "Target Linkname", "Source Linkname"]
REQ_METRIC_VIOLATION_HEADERS = ["Metric", "Description", "Path", "Line", "Value", "Min", "Max",
                                "Severity"]

CSV_SEPARATOR = ";"


def __compatible(headers, required):
    return all(req in headers for req in required)


def convert_file(path, version):
    if not os.path.isfile(path):
        return []

    content = ""
    with open(path, "r", newline="") as f:
        content = f.read()

    if len(content) > 0:
        return convert_text(content, version)
    return []


def convert_text(content, version, filter_suppressed=True):
    output = []
    if content:
        reader = csv.reader(content.strip().split("\n"), delimiter=";", )

        headers = []
        entries = []
        filters = []
        if filter_suppressed:
            filters.append(lambda row, headers: row[headers.index("Suppressed")].lower() == "true")

        for line_num, row in enumerate(reader):
            if line_num == 0:
                headers = row
            else:
                # will evaluate all filters regardless of prior results
                # this is fine for now, but maybe split this up into separate steps
                # if slower filters are introduced
                if any([f(row, headers) for f in filters]):
                    break
                entries.append(row)

        if __compatible(headers, REQ_STYLE_VIOLATION_HEADERS):
            output = __convert_style_violations(headers, entries)
        elif __compatible(headers, REQ_ARCHITECTURE_VIOLATION_HEADERS):
            output = __convert_architecture_violations(headers, entries)
        elif __compatible(headers, REQ_METRIC_VIOLATION_HEADERS):
            output = __convert_metric_violations(headers, entries)

    return output


def __convert_style_violations(headers, entries):
    violations = []
    for token in entries:
        filename = token[headers.index("Path")]
        line_num = token[headers.index("Line")]
        message = token[headers.index("Message")]
        severity = token[headers.index("Severity")]
        error_num = token[headers.index("Error Number")]

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


def __convert_architecture_violations(headers, entries):
    violations = []
    for token in entries:
        filename = token[headers.index("Source Path")]
        line_num = token[headers.index("Source Line")]
        source_link = token[headers.index("Source Linkname")]
        target_link = token[headers.index("Target Linkname")]
        violation_type = token[headers.index("Violation Type")]

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


def __convert_metric_violations(headers, entries):
    violations = []
    for token in entries:
        filename = token[headers.index("Path")]
        line_num = token[headers.index("Line")]
        severity = token[headers.index("Severity")]
        metric = token[headers.index("Metric")]
        desc = token[headers.index("Description")]
        min_val = token[headers.index("Min")]
        max_val = token[headers.index("Max")]
        val = token[headers.index("Value")]

        if line_num.isdigit():
            line_num = max(0, int(line_num))
        else:
            line_num = 0

        text = ""
        if metric and desc:
            text = metric + " (" + desc + ")"
        elif metric:
            text = metric
        elif desc:
            text = desc

        if text and val:
            text += f": {val}."
            if min_val and max_val:
                text += f" Allowed range: [{min_val}, {max_val}]"

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
        violation["nr"] = metric

        violations.append(violation)
    return violations
