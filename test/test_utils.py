"""Test functions from utils.py"""

from form_manager import utils

BASE_TEMPLATE = """{{ val }} random text here 12345 {{ }}.
more text here {{ asd }} {{ val }}
{{
  bad_variable
}}

Text here {{ {{ spec_val }} }}

{{ variable }}"""


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
    assert res.count("hit_1") == 2
    assert res.count("hit_2") == 1
    assert "BAD" not in data
    assert "unique }}" not in data
