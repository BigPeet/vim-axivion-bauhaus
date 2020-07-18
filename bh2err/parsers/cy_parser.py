import bh2err.parsers.base_parser as base_parser


class CYParser(base_parser.BaseParser):

    mapping = {
      "Dependency Type": "dependency_type",
      "Source Path": "filename",
      "Source Line": "line_num",
      "Source Linkname": "source_link",
      "Target Linkname": "target_link",
      }

    @classmethod
    def header_field_mapping(cls):
        return cls.mapping

    @classmethod
    def process_tokens(cls, parsed_tokens):
        violations = []
        if parsed_tokens:
            line_num = cls.sanitize_line(parsed_tokens["line_num"])
            source_link = parsed_tokens["source_link"]
            target_link = parsed_tokens["target_link"]
            dependency_type = parsed_tokens["dependency_type"]

            text = ""
            if source_link and target_link:
                text = source_link + " -> " + target_link
            elif source_link:
                text = source_link

            violation = dict()
            violation["filename"] = parsed_tokens["filename"]
            violation["lnum"] = line_num
            violation["text"] = text
            if dependency_type:
                violation["type"] = "E"
            else:
                violation["type"] = ""
            violations.append(violation)

        return violations
