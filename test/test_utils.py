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
    print(res)
    assert res.count("hit_1") == 2
    assert res.count("hit_2") == 1
    assert "BAD" not in data
    assert "unique }}" not in data


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
