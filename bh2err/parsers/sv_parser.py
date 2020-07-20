import bh2err.parsers.base_parser as base_parser


class SVParser(base_parser.BaseParser):

    mapping = {
      "Path": "filename",
      "Line": "line_num",
      "Message": "message",
      "Severity": "severity",
      "Error Number": "error_num"
      }

    @classmethod
    def header_field_mapping(cls):
        return cls.mapping

    @classmethod
    def process_tokens(cls, parsed_tokens):
        violations = []
        if parsed_tokens:
            filename = parsed_tokens["filename"]
            if len(filename) > 0:
                line_num = cls.sanitize_line(parsed_tokens["line_num"])
                error_num = parsed_tokens["error_num"]
                message = parsed_tokens["message"]
                severity = parsed_tokens["severity"]

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
