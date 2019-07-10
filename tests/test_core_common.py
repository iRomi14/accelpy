# coding=utf-8
"""Common functions tests"""


def test_recursive_update():
    """Tests test_recursive_update"""
    from accelpy._common import recursive_update

    to_update = {'root1': {'key1': 1, 'key2': 2}, 'key3': 3}
    update = {'root1': {'key1': 1.0, 'key4': 4.0}, 'key5': 5.0, 'key6': {}}
    expected = {'root1': {'key1': 1.0, 'key2': 2, 'key4': 4.0},
                'key3': 3, 'key5': 5.0, 'key6': {}}

    assert recursive_update(to_update, update) == expected
