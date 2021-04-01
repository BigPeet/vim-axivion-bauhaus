import os.path
import csv
from bh2err.parsers import Parsers
from bh2err.filters import parse_filters

CSV_SEPARATOR = ";"


def convert_file(path, version, filters=[]):
    if not os.path.isfile(path):
        return []

    content = ""
    with open(path, "r", newline="") as f:
        content = f.read()

    if len(content) > 0:
        return convert_text(content, version, filters)
    return []


def convert_text(content, version, input_filters=[], filter_suppressed=True):
    if content:
        reader = csv.reader(content.strip().split("\n"), delimiter=CSV_SEPARATOR, )

        headers = []
        entries = []

        # parse input filters
        filters = parse_filters(input_filters)

        # Add suppressed filter
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
                    continue
                entries.append(row)

        for parser in Parsers:
            if parser.is_compatible(headers):
                return parser.parse(headers, entries)

    return []
