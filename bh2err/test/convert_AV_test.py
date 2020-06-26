import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)
ARCHITECTURE_VIOLATION_HEADERS = '"Id";"State";"Suppressed";"Violation Type";"Architecture Source";'\
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
    content = ARCHITECTURE_VIOLATION_HEADERS + "\n" + 22 * '"";' + '""'
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

    dicts = bh2err.convert_text(ARCHITECTURE_VIOLATION_HEADERS + "\n" + negative_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(ARCHITECTURE_VIOLATION_HEADERS + "\n" + nonexistent_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(ARCHITECTURE_VIOLATION_HEADERS + "\n" + nan_line_num, "")
    assert dicts[0]["lnum"] == 0
