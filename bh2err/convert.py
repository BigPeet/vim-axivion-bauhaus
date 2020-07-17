import os.path
import csv

REQ_STYLE_VIOLATION_HEADERS = ["Error Number", "Message", "Path", "Line", "Severity"]
REQ_ARCHITECTURE_VIOLATION_HEADERS = ["Violation Type", "Source Path", "Source Line",
                                      "Target Linkname", "Source Linkname"]
REQ_METRIC_VIOLATION_HEADERS = ["Metric", "Description", "Path", "Line", "Value", "Min", "Max",
                                "Severity"]
REQ_DEAD_CODE_HEADERS = ["Linkname", "Path", "Line"]
REQ_CLONE_HEADERS = ["Left Path", "Left Line", "Right Path", "Right Line"]
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
        elif __compatible(headers, REQ_DEAD_CODE_HEADERS):
            output = __convert_dead_code_violations(headers, entries)
        elif __compatible(headers, REQ_CLONE_HEADERS):
            output = __convert_clone_violations(headers, entries)

    return output


def __sanitize_line(line_num):
    if line_num.isdigit():
        return max(0, int(line_num))
    return 0


def __convert_style_violations(headers, entries):
    violations = []
    for token in entries:
        filename = token[headers.index("Path")]
        line_num = token[headers.index("Line")]
        message = token[headers.index("Message")]
        severity = token[headers.index("Severity")]
        error_num = token[headers.index("Error Number")]

        line_num = __sanitize_line(line_num)

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

        line_num = __sanitize_line(line_num)

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

        line_num = __sanitize_line(line_num)

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


def __convert_dead_code_violations(headers, entries):
    violations = []
    for token in entries:
        filename = token[headers.index("Path")]
        line_num = token[headers.index("Line")]
        link_name = token[headers.index("Linkname")]

        line_num = __sanitize_line(line_num)

        text = ""
        if link_name:
            text = link_name

        violation = dict()
        violation["filename"] = filename
        violation["lnum"] = line_num
        violation["text"] = text
        violations.append(violation)
    return violations


def __convert_clone_violations(headers, entries):
    violations = []
    for token in entries:
        left_path = token[headers.index("Left Path")]
        left_line = token[headers.index("Left Line")]
        right_path = token[headers.index("Right Path")]
        right_line = token[headers.index("Right Line")]

        left_line = __sanitize_line(left_line)
        right_line = __sanitize_line(right_line)

        left_text = ""
        right_text = ""
        if left_path:
            if right_path:
                if right_path == left_path:
                    left_text = "Clone at line " + str(right_line)
                else:
                    left_text = "Clone of " + right_path + ":" + str(right_line)
                left_text += " (next item)"
            else:
                left_text = "Cloned entity."
        if right_path:
            if left_path:
                if right_path == left_path:
                    right_text = "Clone at line " + str(left_line)
                else:
                    right_text = "Clone of " + left_path + ":" + str(left_line)
                right_text += " (previous item)"
            else:
                right_text = "Cloned entity."

        if left_text:
            left_violation = dict()
            left_violation["filename"] = left_path
            left_violation["lnum"] = left_line
            left_violation["text"] = left_text
            violations.append(left_violation)

        if right_text:
            right_violation = dict()
            right_violation["filename"] = right_path
            right_violation["lnum"] = right_line
            right_violation["text"] = right_text
            violations.append(right_violation)
    return violations
