from .enums import Classification, PowerFactor


def parse_classification_string(s: str) -> Classification:
    match s.strip().lower():
        case ["gm", "grandmaster", "g"]:
            return Classification.GM
        case ["m", "master"]:
            return Classification.M
        case "a":
            return Classification.A
        case "b":
            return Classification.B
        case "c":
            return Classification.C
        case "d":
            return Classification.D
        case ["u", "x"]:
            return Classification.U
        case _:
            return Classification.UNKNOWN


def parse_power_factor(s: str) -> PowerFactor:
    match s.strip().lower():
        case "major":
            return PowerFactor.MAJOR
        case "minor":
            return PowerFactor.MINOR
        case _:
            return PowerFactor.UNKNOWN
