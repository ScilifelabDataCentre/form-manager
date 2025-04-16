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


def test_is_blacklisted_match():
    """Confirm that is_blacklisted detects a match."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"key2": "[0-9]"}]

    assert utils.is_blacklisted(bl_data, bl)


def test_is_blacklisted_no_match():
    """Confirm that is_blacklisted does not report a match when there is none."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"key2": "[a-zA-Z]"}]

    assert not utils.is_blacklisted(bl_data, bl)


def test_is_blacklisted_key_not_present():
    """Confirm that is_blacklisted does not have issues with non-existing keys."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"characters": "[a-zA-Z]"}]

    assert not utils.is_blacklisted(bl_data, bl)


def test_is_blacklisted_key_or_match():
    """Confirm that is_blacklisted detects a match when one part of an or bl matches."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"key2": "[a-zA-Z]"}, {"key": "[a-zA-Z]"}]

    assert utils.is_blacklisted(bl_data, bl)


def test_is_blacklisted_key_or_no_match():
    """Confirm that is_blacklisted detects no match when neither or statement is a match."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"key2": "[a-zA-Z]"}, {"key": "[1-9]"}]

    assert not utils.is_blacklisted(bl_data, bl)


def test_is_blacklisted_key_and_no_match():
    """Confirm that is_blacklisted detects no match when not both statements are correct in AND."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"key": "[a-zA-Z]", "key2": "[a-zA-Z]"}]

    assert not utils.is_blacklisted(bl_data, bl)


def test_is_blacklisted_key_and_match():
    """Confirm that is_blacklisted detects a match when both statements in AND are matching."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"key": "[a-zA-Z]", "key2": "[1-9]"}]

    assert utils.is_blacklisted(bl_data, bl)


def test_is_blacklisted_bad_regex():
    """Confirm that is_blacklisted detects a match when both statements in AND are matching."""
    bl_data = {"key": "value", "key2": "156"}
    bl = [{"key": "(?)"}]

    with pytest.raises(ValueError):
        utils.is_blacklisted(bl_data, bl)
