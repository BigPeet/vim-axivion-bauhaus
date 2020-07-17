import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)
CL_HEADER_STR = '"Id";"State";"Suppressed";"Clone Type";"Left Path";"Left Line";"Left End Line";'\
        '"Left Length";"Left Weight";"Right Path";"Right Line";"Right End Line";"Right Length";'\
        '"Right Weight";"Justification";"Tags"'


def test_CL_sane_examples():
    path = DIRECTORY + "/CL_sane_examples.csv"
    file_dicts = bh2err.convert_file(path, "")
    content_dicts = []

    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "")

    assert file_dicts != []
    assert len(file_dicts) == 6
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/test.c"
    assert file_dicts[0]["lnum"] == 100
    assert file_dicts[0]["text"] == "Clone at line 200 (next item)"

    assert file_dicts[1]["filename"] == "test/test.c"
    assert file_dicts[1]["lnum"] == 200
    assert file_dicts[1]["text"] == "Clone at line 100 (previous item)"

    assert file_dicts[2]["filename"] == "test/test.h"
    assert file_dicts[2]["lnum"] == 123
    assert file_dicts[2]["text"] == "Clone of test/another.h:123 (next item)"

    assert file_dicts[3]["filename"] == "test/another.h"
    assert file_dicts[3]["lnum"] == 123
    assert file_dicts[3]["text"] == "Clone of test/test.h:123 (previous item)"

    assert file_dicts[4]["filename"] == "real/test.c"
    assert file_dicts[4]["lnum"] == 42
    assert file_dicts[4]["text"] == "Cloned entity."

    assert file_dicts[5]["filename"] == "real/config.c"
    assert file_dicts[5]["lnum"] == 123
    assert file_dicts[5]["text"] == "Cloned entity."


def test_CL_empty_entry():
    content = CL_HEADER_STR + "\n" + 15 * '"";' + '""'
    dicts = bh2err.convert_text(content, "")
    assert len(dicts) == 0


def test_CL_invalid_line_num():
    line_num_pattern = 4 * '"";' + '"left-path";' + '"{}";' + 3 * '"";' + '"right-path";'\
            + '"{}";' + 4 * '"";' + '""'
    lnegative_line_num = line_num_pattern.format(-13, 42)
    lnonexistent_line_num = line_num_pattern.format("", 42)
    lnan_line_num = line_num_pattern.format("test", 42)
    rnegative_line_num = line_num_pattern.format(42, -13)
    rnonexistent_line_num = line_num_pattern.format(42, "")
    rnan_line_num = line_num_pattern.format(42, "test")

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + lnegative_line_num, "")
    assert dicts[0]["lnum"] == 0
    assert dicts[1]["lnum"] == 42

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + lnonexistent_line_num, "")
    assert dicts[0]["lnum"] == 0
    assert dicts[1]["lnum"] == 42

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + lnan_line_num, "")
    assert dicts[0]["lnum"] == 0
    assert dicts[1]["lnum"] == 42

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + rnegative_line_num, "")
    assert dicts[0]["lnum"] == 42
    assert dicts[1]["lnum"] == 0

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + rnonexistent_line_num, "")
    assert dicts[0]["lnum"] == 42
    assert dicts[1]["lnum"] == 0

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + rnan_line_num, "")
    assert dicts[0]["lnum"] == 42
    assert dicts[1]["lnum"] == 0


def test_CL_suppressed_violations():
    line_pattern = 2 * '"";' + '"{}";"";"left-path";' + 4 * '"";' + '"right-path";'\
            + 5 * '"";' + '""'
    suppressed_false = line_pattern.format("false")
    suppressed_true = line_pattern.format("true")
    suppressed_none = line_pattern.format("")

    print(suppressed_false)
    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_false, "")
    assert len(dicts) == 2
    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_none, "")
    assert len(dicts) == 2
    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_true, "")
    assert len(dicts) == 0

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_false, "", filter_suppressed=True)
    assert len(dicts) == 2
    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=True)
    assert len(dicts) == 2
    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=True)
    assert len(dicts) == 0

    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_false,
                                "", filter_suppressed=False)
    assert len(dicts) == 2
    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=False)
    assert len(dicts) == 2
    dicts = bh2err.convert_text(CL_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=False)
    assert len(dicts) == 2
