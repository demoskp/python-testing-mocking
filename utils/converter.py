class UnsupportedDistanceUnit(Exception):
    pass


def distance_converter(value: float, from_unit: str, to_unit: str) -> float:
    units = {
        "miles": {
            "kilometers": 1.609344,
            "feet": 5280,
        },
        "kilometers": {
            "miles": 0.621371,
            "feet": 3280.839895,
        },
        "feet": {
            "miles": 0.000189,
            "kilometers": 0.000305,
        },
    }

    supported_units = list(units.keys()) + ["miles"]

    if from_unit not in supported_units:
        raise UnsupportedDistanceUnit(f"Unit: {from_unit} is not supported")

    if to_unit not in supported_units:
        raise UnsupportedDistanceUnit(f"Unit: {to_unit} is not supported")

    if from_unit == to_unit:
        return value

    return units.get(from_unit).get(to_unit) * value
