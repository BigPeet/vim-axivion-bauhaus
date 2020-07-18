import bh2err.parsers.base_parser as base_parser


class MVParser(base_parser.BaseParser):

    mapping = {
      "Path": "filename",
      "Line": "line_num",
      "Severity": "severity",
      "Metric": "metric",
      "Description": "desc",
      "Min": "min_val",
      "Max": "max_val",
      "Value": "val"
      }

    @classmethod
    def header_field_mapping(cls):
        return cls.mapping

    @classmethod
    def process_tokens(cls, parsed_tokens):
        violations = []
        if parsed_tokens:
            line_num = cls.sanitize_line(parsed_tokens["line_num"])
            severity = parsed_tokens["severity"]
            metric = parsed_tokens["metric"]
            desc = parsed_tokens["desc"]
            min_val = parsed_tokens["min_val"]
            max_val = parsed_tokens["max_val"]
            val = parsed_tokens["val"]

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
            violation["filename"] = parsed_tokens["filename"]
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
