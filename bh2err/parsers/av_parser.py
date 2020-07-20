import bh2err.parsers.base_parser as base_parser


class AVParser(base_parser.BaseParser):

    mapping = {
      "Source Path": "filename",
      "Source Line": "line_num",
      "Source Linkname": "source_link",
      "Target Linkname": "target_link",
      "Violation Type": "violation_type"
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
                source_link = parsed_tokens["source_link"]
                target_link = parsed_tokens["target_link"]
                violation_type = parsed_tokens["violation_type"]

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
