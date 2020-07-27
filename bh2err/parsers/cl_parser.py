from .base_parser import BaseParser


class CLParser(BaseParser):

    mapping = {
      "Left Path": "left_path",
      "Left Line": "left_line",
      "Right Path": "right_path",
      "Right Line": "right_line",
      }

    @classmethod
    def header_field_mapping(cls):
        return cls.mapping

    @classmethod
    def process_tokens(cls, parsed_tokens):
        violations = []
        if parsed_tokens:
            left_line = cls.sanitize_line(parsed_tokens["left_line"])
            right_line = cls.sanitize_line(parsed_tokens["right_line"])
            left_path = parsed_tokens["left_path"]
            right_path = parsed_tokens["right_path"]

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
