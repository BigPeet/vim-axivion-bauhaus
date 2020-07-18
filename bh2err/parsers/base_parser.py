class BaseParser:

    @classmethod
    def parse(cls, headers, entries):
        violations = []
        for entry in entries:
            tokens = cls.parse_entry(headers, entry)
            violations.extend(cls.process_tokens(tokens))
        return violations

    @classmethod
    def parse_entry(cls, headers, entry):
        tokens = None
        if headers and entry:
            tokens = dict()
            for header, field in cls.header_field_mapping().items():
                tokens[field] = entry[headers.index(header)]
        return tokens

    @staticmethod
    def sanitize_line(line_num):
        if line_num.isdigit():
            return max(0, int(line_num))
        return 0

    @classmethod
    def is_compatible(cls, headers):
        req_headers = cls.required_headers()
        return len(req_headers) > 0 and all(req in headers for req in req_headers)

    @classmethod
    def priority(cls):
        return len(cls.required_headers())

    @classmethod
    def required_headers(cls):
        return cls.header_field_mapping().keys()

    @classmethod
    def process_tokens(cls, parsed_tokens):
        raise NotImplementedError

    @classmethod
    def header_field_mapping(cls):
        raise NotImplementedError
