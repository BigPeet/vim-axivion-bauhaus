import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)
SV_HEADER_STR = '"Id";"State";"Suppressed";"Error Number";"Message";"Entity";'\
    '"Path";"Line";"Provider";"Severity";"Justification";"Tags"'


def test_SV_sane_examples():
    path = DIRECTORY + "/SV_sane_examples.csv"
    file_dicts = bh2err.convert_file(path, "")
    content_dicts = []

    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "")

    assert file_dicts != []
    assert len(file_dicts) == 5
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 37
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[1]["filename"] == "test/file.c"
    assert file_dicts[1]["lnum"] == 120
    assert file_dicts[1]["type"] == "W"
    assert file_dicts[1]["text"] == "Error 12312: Test"

    assert file_dicts[2]["filename"] == "test/file.h"
    assert file_dicts[2]["lnum"] == 42
    assert file_dicts[2]["type"] == "E"
    assert file_dicts[2]["text"] == "ABC: asdf"

    assert file_dicts[3]["filename"] == "real/file.c"
    assert file_dicts[3]["lnum"] == 49
    assert file_dicts[3]["type"] == "W"
    assert file_dicts[3]["text"] == "You didn't say the magic word."

    assert file_dicts[4]["filename"] == "test/config.c"
    assert file_dicts[4]["lnum"] == 0
    assert file_dicts[4]["type"] == "E"
    assert file_dicts[4]["text"] == "Error 42: You didn't say the magic word."


def test_SV_empty_entry():
    content = SV_HEADER_STR + "\n" + 11 * '"";' + '""'
    dicts = bh2err.convert_text(content, "")
    assert len(dicts) == 0


def test_SV_invalid_line_num():
    line_num_pattern = 6 * '"";' + '"path";"{}";' + 3 * '"";' + '""'
    negative_line_num = line_num_pattern.format(-13)
    nonexistent_line_num = line_num_pattern.format("")
    nan_line_num = line_num_pattern.format("test")

    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + negative_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + nonexistent_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + nan_line_num, "")
    assert dicts[0]["lnum"] == 0


def test_SV_semicolon_and_linebreak_in_text():
    msg = 'Message ; \\n interrupted; by ; and \\n; '
    content = 4 * '"";' + '"' + msg + '";"";"path;"' + 4 * '"";' + '""'
    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + content, "")
    assert len(dicts) == 1
    assert dicts[0]["text"] == msg


def test_SV_suppressed_violations():
    line_pattern = 2 * '"";' + '"{}";' + 3 * '"";' + '"path";' + 4 * '"";' + '""'
    suppressed_false = line_pattern.format("false")
    suppressed_true = line_pattern.format("true")
    suppressed_none = line_pattern.format("")

    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_false, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_none, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_true, "")
    assert len(dicts) == 0

    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_false, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=True)
    assert len(dicts) == 0

    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_false,
                                "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(SV_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=False)
    assert len(dicts) == 1
