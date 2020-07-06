import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)
AV_HEADER_STR = '"Id";"State";"Suppressed";"Violation Type";"Architecture Source";'\
                                  '"Architecture Source Linkname";"Architecture Source Type";"Architecture Target";'\
                                  '"Architecture Target Linkname";"Architecture Target Type";"Source Entity";'\
                                  '"Source Linkname";"Source Entity Type";"Source Path";"Source Line";'\
                                  '"Dependency Type";"Target Entity";"Target Linkname";"Target Entity Type";'\
                                  '"Target Path";"Target Line";"Justification";"Tags"'


def test_AV_sane_examples():
    path = DIRECTORY + "/AV_sane_examples.csv"
    file_dicts = bh2err.convert_file(path, "")
    content_dicts = []

    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "")

    assert file_dicts != []
    assert len(file_dicts) == 3
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.h"
    assert file_dicts[0]["lnum"] == 42
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "T custom:size_type -> T std:some_size"

    assert file_dicts[1]["filename"] == "test/file.h"
    assert file_dicts[1]["lnum"] == 100
    assert file_dicts[1]["type"] == "W"
    assert file_dicts[1]["text"] == "S custom:tag -> S std:some_tag"

    assert file_dicts[2]["filename"] == "test/file.h"
    assert file_dicts[2]["lnum"] == 42
    assert file_dicts[2]["type"] == ""
    assert file_dicts[2]["text"] == "T custom:size_type -> T std:some_size"


def test_AV_empty_entry():
    content = AV_HEADER_STR + "\n" + 22 * '"";' + '""'
    print(content)
    dicts = bh2err.convert_text(content, "")
    assert len(dicts) == 1
    assert dicts[0]["filename"] == ""
    assert dicts[0]["lnum"] == 0
    assert dicts[0]["type"] == ""
    assert dicts[0]["text"] == ""


def test_AV_invalid_line_num():
    line_num_pattern = 14 * '"";' + '"{}";' + 7 * '"";' + '""'
    negative_line_num = line_num_pattern.format(-13)
    nonexistent_line_num = line_num_pattern.format("")
    nan_line_num = line_num_pattern.format("test")

    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + negative_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + nonexistent_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + nan_line_num, "")
    assert dicts[0]["lnum"] == 0


def test_AV_suppressed_violations():
    line_pattern = 2 * '"";' + '"{}";' + 19 * '"";' + '""'
    suppressed_false = line_pattern.format("false")
    suppressed_true = line_pattern.format("true")
    suppressed_none = line_pattern.format("")

    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_false, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_none, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_true, "")
    assert len(dicts) == 0

    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_false, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=True)
    assert len(dicts) == 0

    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_false, "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(AV_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=False)
    assert len(dicts) == 1
