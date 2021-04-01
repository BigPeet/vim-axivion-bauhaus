import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)
CY_HEADER_STR = '"Id";"State";"Suppressed";"Source Entity";"Source Linkname";'\
        '"Source Entity Type";"Dependency Type";"Source Path";"Source Line";'\
        '"Target Entity";"Target Linkname";"Target Entity Type";"Target Path";'\
        '"Target Line";"Justification";"Tags"'


def test_CY_sane_examples():
    path = DIRECTORY + "/CY_sane_examples.csv"
    file_dicts = bh2err.convert_file(path, "")
    content_dicts = []

    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "")

    assert file_dicts != []
    assert len(file_dicts) == 6
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 42
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "class A -> struct H"

    assert file_dicts[1]["filename"] == "test/file.c"
    assert file_dicts[1]["lnum"] == 42
    assert file_dicts[1]["type"] == ""
    assert file_dicts[1]["text"] == "class A -> struct H"

    assert file_dicts[2]["filename"] == "test/file.c"
    assert file_dicts[2]["lnum"] == 42
    assert file_dicts[2]["type"] == "E"
    assert file_dicts[2]["text"] == ""

    assert file_dicts[3]["filename"] == "test/file.c"
    assert file_dicts[3]["lnum"] == 42
    assert file_dicts[3]["type"] == "E"
    assert file_dicts[3]["text"] == ""

    assert file_dicts[4]["filename"] == "test/file.c"
    assert file_dicts[4]["lnum"] == 42
    assert file_dicts[4]["type"] == ""
    assert file_dicts[4]["text"] == "class A"

    assert file_dicts[5]["filename"] == "test/file.c"
    assert file_dicts[5]["lnum"] == 42
    assert file_dicts[5]["type"] == ""
    assert file_dicts[5]["text"] == "class A"


def test_CY_empty_entry():
    content = CY_HEADER_STR + "\n" + 15 * '"";' + '""'
    print(content)
    dicts = bh2err.convert_text(content, "")
    assert len(dicts) == 0


def test_CY_invalid_line_num():
    line_num_pattern = 7 * '"";' + '"path";"{}";' + 6 * '"";' + '""'
    negative_line_num = line_num_pattern.format(-13)
    nonexistent_line_num = line_num_pattern.format("")
    nan_line_num = line_num_pattern.format("test")

    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + negative_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + nonexistent_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + nan_line_num, "")
    assert dicts[0]["lnum"] == 0


def test_CY_suppressed_violations():
    line_pattern = 2 * '"";' + '"{}";' + 4 * '"";' + '"path";' + 7 * '"";' + '""'
    suppressed_false = line_pattern.format("false")
    suppressed_true = line_pattern.format("true")
    suppressed_none = line_pattern.format("")

    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_false, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_none, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_true, "")
    assert len(dicts) == 0

    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_false, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=True)
    assert len(dicts) == 0

    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_false,
                                "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(CY_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=False)
    assert len(dicts) == 1
