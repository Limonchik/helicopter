import pytest

from utils.utils import *


class TestUtilsClass:
    def test_stringified_lists_in_dict(self):
        dictionary = {
            "list": [1, 2, 3],
            "other_dict": {
                "other_list": [4, 5, 6],
                "random_key": True
            }
        }
        result_dictionary = {
            "list": json.dumps([1, 2, 3]),
            "other_dict": {
                "other_list": json.dumps([4, 5, 6]),
                "random_key": True
            }
        }

        stringify_lists_in_dict(dictionary)
        assert dictionary == result_dictionary

    def test_random_chance_always_true(self):

        chance = 1

        for i in range(100):
            assert random_chance(chance)

    def test_random_chance_never_true(self):
        chance = 0
        for i in range(100):
            assert not random_chance(chance)

    def test_random_chance_50_percents(self):
        chance = 0.5
        inaccuracy = 0
        acceptable_error_margin_percentage = 0.05
        selection = 2000
        for i in range(selection):
            if random_chance(chance):
                inaccuracy += 1
            else:
                inaccuracy -= 1

        assert abs(inaccuracy) <= acceptable_error_margin_percentage * selection

    def test_neighboring_cord_valid_args(self):
        selection = 10
        width, height = 10, 10
        x, y = 5, 5
        for i in range(selection):
            x, y = neighboring_cord(x, y, width, height)
            assert (0 <= x < width) and (0 <= y < height)

    def test_neighboring_cord_invalid_cord(self):
        width, height = 10, 10
        x, y = -3, -2
        with pytest.raises(InvalidArgsException) as exc_info:
            neighboring_cord(x, y, width, height)

        assert exc_info.type is InvalidArgsException

    def test_random_cord(self):
        width, height = 10, 10
        x, y = random_cord(width, height)
        assert 0 <= x <= width and 0 <= y <= height
