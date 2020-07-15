import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)
MV_HEADER_STR = '"Id";"State";"Suppressed";"Metric";"Description";"Entity";"Linkname";'\
                '"Entity Type";"Path";"Line";"Value";"Min";"Max";"Severity";"Justification";"Tags"'


def test_MV_sane_examples():
    path = DIRECTORY + "/MV_sane_examples.csv"
    file_dicts = bh2err.convert_file(path, "")
    content_dicts = []

    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "")

    assert file_dicts != []
    assert len(file_dicts) == 8
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 81
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "Metric.HIS.PATH (HIS PATH): 42.0. Allowed range: [1.0, 30.0]"

    assert file_dicts[1]["filename"] == "test/file.c"
    assert file_dicts[1]["lnum"] == 33
    assert file_dicts[1]["type"] == "W"
    assert file_dicts[1]["text"] == "Metric.HIS.RETURN (HIS RETURN): 6.0. Allowed range: [0.0, 2.0]"

    assert file_dicts[2]["filename"] == "test/file.h"
    assert file_dicts[2]["lnum"] == 41
    assert file_dicts[2]["type"] == ""
    assert file_dicts[2]["text"] == "Response for a class: 54.0. Allowed range: [0.0, 40.0]"

    assert file_dicts[3]["filename"] == "real/file.c"
    assert file_dicts[3]["lnum"] == 123
    assert file_dicts[3]["type"] == "E"
    assert file_dicts[3]["text"] == "Metric.OO.WMC.One: 42.0. Allowed range: [0.0, 20.0]"

    assert file_dicts[4]["filename"] == "test/config.c"
    assert file_dicts[4]["lnum"] == 0
    assert file_dicts[4]["type"] == "E"
    assert file_dicts[4]["text"] == "Metric.OO.WMC.One (Weighted Methods per Class based on 1): "\
                                    " 28.0. Allowed range: [0.0, 15.0]"

    assert file_dicts[5]["filename"] == "test/file.c"
    assert file_dicts[5]["lnum"] == 33
    assert file_dicts[5]["type"] == "W"
    assert file_dicts[5]["text"] == "Metric.HIS.RETURN (HIS RETURN)"

    assert file_dicts[6]["filename"] == "test/file.c"
    assert file_dicts[6]["lnum"] == 33
    assert file_dicts[6]["type"] == "W"
    assert file_dicts[6]["text"] == "Metric.HIS.RETURN (HIS RETURN): 6.0."

    assert file_dicts[7]["filename"] == "test/file.c"
    assert file_dicts[7]["lnum"] == 33
    assert file_dicts[7]["type"] == "W"
    assert file_dicts[7]["text"] == "Metric.HIS.RETURN (HIS RETURN): 6.0."


def test_MV_empty_entry():
    content = MV_HEADER_STR + "\n" + 15 * '"";' + '""'
    dicts = bh2err.convert_text(content, "")
    assert len(dicts) == 1
    assert dicts[0]["filename"] == ""
    assert dicts[0]["lnum"] == 0
    assert dicts[0]["type"] == ""
    assert dicts[0]["text"] == ""


def test_MV_invalid_line_num():
    line_num_pattern = 9 * '"";' + '"{}";' + 5 * '"";' + '""'
    negative_line_num = line_num_pattern.format(-13)
    nonexistent_line_num = line_num_pattern.format("")
    nan_line_num = line_num_pattern.format("test")

    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + negative_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + nonexistent_line_num, "")
    assert dicts[0]["lnum"] == 0

    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + nan_line_num, "")
    assert dicts[0]["lnum"] == 0


def test_MV_suppressed_violations():
    line_pattern = 2 * '"";' + '"{}";' + 12 * '"";' + '""'
    suppressed_false = line_pattern.format("false")
    suppressed_true = line_pattern.format("true")
    suppressed_none = line_pattern.format("")

    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_false, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_none, "")
    assert len(dicts) == 1
    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_true, "")
    assert len(dicts) == 0

    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_false, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=True)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=True)
    assert len(dicts) == 0

    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_false,
                                "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_none, "", filter_suppressed=False)
    assert len(dicts) == 1
    dicts = bh2err.convert_text(MV_HEADER_STR + "\n" + suppressed_true, "", filter_suppressed=False)
    assert len(dicts) == 1
