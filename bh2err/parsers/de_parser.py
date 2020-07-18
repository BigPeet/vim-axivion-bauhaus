import bh2err.parsers.base_parser as base_parser


class DEParser(base_parser.BaseParser):

    mapping = {
      "Path": "filename",
      "Line": "line_num",
      "Linkname": "link_name",
      }

    @classmethod
    def header_field_mapping(cls):
        return cls.mapping

    @classmethod
    def process_tokens(cls, parsed_tokens):
        violations = []
        if parsed_tokens:
            line_num = cls.sanitize_line(parsed_tokens["line_num"])
            link_name = parsed_tokens["link_name"]

            text = ""
            if link_name:
                text = link_name

            violation = dict()
            violation["filename"] = parsed_tokens["filename"]
            violation["lnum"] = line_num
            violation["text"] = text
            violations.append(violation)
        return violations
