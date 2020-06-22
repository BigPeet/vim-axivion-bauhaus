import bh2err
import os.path

DIRECTORY = os.path.dirname(__file__)


def test_non_existent_file():
    assert bh2err.convert_file(DIRECTORY + "/BOGUS_FILE", "") == []


def test_malformed_csv():
    pass  # TODO after deciding on csv module step
