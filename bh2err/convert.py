import os.path
import csv
from bh2err.parsers import Parsers

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


def convert_text(content, version, filter_suppressed=True):
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

        for parser in Parsers:
            if parser.is_compatible(headers):
                return parser.parse(headers, entries)

    return []
