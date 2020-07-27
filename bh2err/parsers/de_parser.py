from .base_parser import BaseParser


class DEParser(BaseParser):

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
            filename = parsed_tokens["filename"]
            if len(filename) > 0:
                line_num = cls.sanitize_line(parsed_tokens["line_num"])
                link_name = parsed_tokens["link_name"]

                text = ""
                if link_name:
                    text = link_name

                violation = dict()
                violation["filename"] = filename
                violation["lnum"] = line_num
                violation["text"] = text
                violations.append(violation)
        return violations
