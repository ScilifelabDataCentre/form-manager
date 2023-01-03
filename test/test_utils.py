"""Test functions from utils.py"""

import pytest

from form_manager import utils

BASE_TEMPLATE = "{{ val }} {{asd}}"
BAD_TEMPLATE = "{{ }}"


def test_apply_template():
    """Test apply_template()."""
    data = {
        "val": "hit_1",
        "asd": "hit_2",
        "variable": "hit_3",
        "spec_val": "unique",
        "bad_variable": "BAD",
    }

    res = utils.apply_template(BASE_TEMPLATE, data)
    assert res == "hit_1 hit_2"
    with pytest.raises(ValueError):
        res = utils.apply_template(BAD_TEMPLATE, data)


def test_gen_json_body():
    """Test gen_json_body()."""
    data = {
        "val": "hit_1",
        "asd": "hit_2",
        "variable": "hit_3",
        "spec_val": "unique",
        "bad_variable": "BAD",
    }

    expected = (
        '{\n  "asd": "hit_2",\n  "bad_variable": "BAD",\n  ',
        '"spec_val": "unique",\n  "val": "hit_1",\n  "variable": "hit_3"\n}',
    )

    res = utils.gen_json_body(data)
    assert res.startswith(expected)
    assert "Submission received:" in res
