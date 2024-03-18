import pytest

from utils.converter import distance_converter, UnsupportedDistanceUnit


class TestDistanceConverter:
    def test_distance_converter_converts_units(self):
        # From miles
        assert distance_converter(1, from_unit="miles", to_unit="kilometers") == 1.609344
        assert distance_converter(1, from_unit="miles", to_unit="feet") == 5280

        # From kilometers
        assert distance_converter(1, from_unit="kilometers", to_unit="miles") == 0.621371
        assert distance_converter(1, from_unit="kilometers", to_unit="feet") == 3280.839895

        # From feet
        assert distance_converter(1, from_unit="feet", to_unit="kilometers") == 0.000305
        assert distance_converter(1, from_unit="feet", to_unit="miles") == 0.000189

        # Same input output
        assert distance_converter(1, from_unit="miles", to_unit="miles") == 1
        assert distance_converter(1, from_unit="kilometers", to_unit="kilometers") == 1
        assert distance_converter(1, from_unit="feet", to_unit="feet") == 1

    def test_converter_unsupported_unit(self):
        with pytest.raises(UnsupportedDistanceUnit):
            distance_converter(10, "miles", "inches")

        with pytest.raises(UnsupportedDistanceUnit):
            distance_converter(10, "inches", "kilometers")

    @pytest.mark.parametrize("value, from_unit, to_unit, expected_value", [
        (1, "miles", "kilometers", 1.609344),
        (1, "miles", "feet", 5280),
        (1, "kilometers", "miles", 0.621371),
        (1, "kilometers", "feet", 3280.839895),
        (1, "feet", "kilometers", 0.000305),
        (1, "feet", "miles", 0.000189),
        (1, "miles", "miles", 1),
        (1, "kilometers", "kilometers", 1),
        (1, "feet", "feet", 1),
    ])
    def test_distance_converter_converts_units_parametrized(self, value, from_unit, to_unit, expected_value):
        assert distance_converter(value, from_unit=from_unit, to_unit=to_unit) == expected_value
