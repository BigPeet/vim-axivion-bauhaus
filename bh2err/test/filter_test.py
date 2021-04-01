import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)


def test_SV_error_filter():
    path = DIRECTORY + "/SV_sane_examples.csv"
    filters = ["error::42"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

    assert file_dicts != []
    assert len(file_dicts) == 3
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 37
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[1]["filename"] == "test/config.c"
    assert file_dicts[1]["lnum"] == 0
    assert file_dicts[1]["type"] == "E"
    assert file_dicts[1]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[2]["filename"] == "test/config.c"
    assert file_dicts[2]["lnum"] == 0
    assert file_dicts[2]["type"] == "E"
    assert file_dicts[2]["text"] == "Error 42: This should be found again."


def test_SV_path_filter():
    path = DIRECTORY + "/SV_sane_examples.csv"
    filters = ["path::test"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

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

    assert file_dicts[3]["filename"] == "test/config.c"
    assert file_dicts[3]["lnum"] == 0
    assert file_dicts[3]["type"] == "E"
    assert file_dicts[3]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[4]["filename"] == "test/config.c"
    assert file_dicts[4]["lnum"] == 0
    assert file_dicts[4]["type"] == "E"
    assert file_dicts[4]["text"] == "Error 42: This should be found again."


def test_SV_severity_filter():
    path = DIRECTORY + "/SV_sane_examples.csv"
    filters = ["severity::high"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

    assert file_dicts != []
    assert len(file_dicts) == 2
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 37
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[1]["filename"] == "test/file.h"
    assert file_dicts[1]["lnum"] == 42
    assert file_dicts[1]["type"] == "E"
    assert file_dicts[1]["text"] == "ABC: asdf"


def test_SV_multiple_patterns_filter():
    path = DIRECTORY + "/SV_sane_examples.csv"
    filters = ["error::42;A"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

    assert file_dicts != []
    assert len(file_dicts) == 4
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 37
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[1]["filename"] == "test/file.h"
    assert file_dicts[1]["lnum"] == 42
    assert file_dicts[1]["type"] == "E"
    assert file_dicts[1]["text"] == "ABC: asdf"

    assert file_dicts[2]["filename"] == "test/config.c"
    assert file_dicts[2]["lnum"] == 0
    assert file_dicts[2]["type"] == "E"
    assert file_dicts[2]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[3]["filename"] == "test/config.c"
    assert file_dicts[3]["lnum"] == 0
    assert file_dicts[3]["type"] == "E"
    assert file_dicts[3]["text"] == "Error 42: This should be found again."


def test_SV_negation_filter():
    path = DIRECTORY + "/SV_sane_examples.csv"
    filters = ["error:-:42"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

    assert file_dicts != []
    assert len(file_dicts) == 3
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 120
    assert file_dicts[0]["type"] == "W"
    assert file_dicts[0]["text"] == "Error 12312: Test"

    assert file_dicts[1]["filename"] == "test/file.h"
    assert file_dicts[1]["lnum"] == 42
    assert file_dicts[1]["type"] == "E"
    assert file_dicts[1]["text"] == "ABC: asdf"

    assert file_dicts[2]["filename"] == "real/file.c"
    assert file_dicts[2]["lnum"] == 49
    assert file_dicts[2]["type"] == "W"
    assert file_dicts[2]["text"] == "You didn't say the magic word."


def test_SV_exact_filter():
    path = DIRECTORY + "/SV_sane_examples.csv"

    filters = ["error:!:42"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

    assert file_dicts == []
    assert content_dicts == []


    filters = ["error:!:Error 42"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

    assert file_dicts != []
    assert len(file_dicts) == 3
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 37
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[1]["filename"] == "test/config.c"
    assert file_dicts[1]["lnum"] == 0
    assert file_dicts[1]["type"] == "E"
    assert file_dicts[1]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[2]["filename"] == "test/config.c"
    assert file_dicts[2]["lnum"] == 0
    assert file_dicts[2]["type"] == "E"
    assert file_dicts[2]["text"] == "Error 42: This should be found again."


def test_SV_wild_combination():
    path = DIRECTORY + "/SV_sane_examples.csv"
    filters = ["error:!-:Error 12312;ABC"]

    file_dicts = bh2err.convert_file(path, "", filters=filters)
    content_dicts = []
    with open(path, "r") as f:
        content = f.read()
        content_dicts = bh2err.convert_text(content, "", input_filters=filters)

    assert file_dicts != []
    assert len(file_dicts) == 5
    assert content_dicts != []
    assert content_dicts == file_dicts

    assert file_dicts[0]["filename"] == "test/file.c"
    assert file_dicts[0]["lnum"] == 37
    assert file_dicts[0]["type"] == "E"
    assert file_dicts[0]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[1]["filename"] == "test/file.h"
    assert file_dicts[1]["lnum"] == 42
    assert file_dicts[1]["type"] == "E"
    assert file_dicts[1]["text"] == "ABC: asdf"

    assert file_dicts[2]["filename"] == "real/file.c"
    assert file_dicts[2]["lnum"] == 49
    assert file_dicts[2]["type"] == "W"
    assert file_dicts[2]["text"] == "You didn't say the magic word."

    assert file_dicts[3]["filename"] == "test/config.c"
    assert file_dicts[3]["lnum"] == 0
    assert file_dicts[3]["type"] == "E"
    assert file_dicts[3]["text"] == "Error 42: You didn't say the magic word."

    assert file_dicts[4]["filename"] == "test/config.c"
    assert file_dicts[4]["lnum"] == 0
    assert file_dicts[4]["type"] == "E"
    assert file_dicts[4]["text"] == "Error 42: This should be found again."
