import decimal
from types import SimpleNamespace

from hitfactorpy.enums import PowerFactor, Scoring

e4 = decimal.Decimal("0.0001")
ZERO_HF = decimal.Decimal().quantize(e4)


class HitFactorTestCases:
    CHRONO = [
        (
            # Minimal valid input
            SimpleNamespace(
                scoring_type="chrono",
                hit_factor=0,
            ),
            decimal.Decimal().quantize(e4),
        ),
        (
            SimpleNamespace(
                scoring_type="chrono",
                hit_factor=6.1234,
            ),
            decimal.Decimal("6.1234").quantize(e4),
        ),
        (
            SimpleNamespace(
                scoring_type=Scoring.CHRONO,
                hit_factor=6.12340000,
            ),
            decimal.Decimal("6.1234").quantize(e4),
        ),
        (
            SimpleNamespace(
                scoring_type="chrono",
                hit_factor=6.123400001,
            ),
            decimal.Decimal("6.1234").quantize(e4),
        ),
    ]
    FIXED_TIME = [
        (
            # Minimal valid input
            SimpleNamespace(
                scoring_type=Scoring.FIXED_TIME,
                a=0,
                c=0,
                d=0,
                m=0,
                ns=0,
            ),
            ZERO_HF,
        ),
        (
            SimpleNamespace(
                scoring_type=Scoring.FIXED_TIME,
                power_factor=PowerFactor.MAJOR,
                a=12,
                c=7,
                d=0,
                m=1,
                ns=1,
                procedural=2,
                time=23.72,
            ),
            decimal.Decimal("2.0236").quantize(e4),
        ),
        (
            SimpleNamespace(
                scoring_type=Scoring.FIXED_TIME,
                power_factor=PowerFactor.MINOR,
                a=12,
                c=7,
                d=0,
                m=1,
                ns=1,
                procedural=2,
                time=23.72,
            ),
            decimal.Decimal("1.7285").quantize(e4),
        ),
        (
            SimpleNamespace(
                scoring_type=Scoring.FIXED_TIME,
                a=7,
                c=9,
                d=3,
                m=1,
                ns=1,
                procedural=0,
                time=24.75,
            ),
            decimal.Decimal("1.8182").quantize(e4),
        ),
    ]
    COMSTOCK = [
        (
            # Minimal valid input
            SimpleNamespace(
                power_factor=PowerFactor.MINOR,
                a=30,
                c=1,
                d=1,
                time=18.7,
            ),
            decimal.Decimal("8.2353").quantize(e4),
        ),
        (
            # Same score, but major power factor
            SimpleNamespace(
                power_factor=PowerFactor.MAJOR,
                dq=False,
                dnf=False,
                a=30,
                c=1,
                d=1,
                m=0,
                ns=0,
                time=18.7,
            ),
            decimal.Decimal("8.3422").quantize(e4),
        ),
        (
            # Minimal input for a DQ
            SimpleNamespace(dq=True),
            ZERO_HF,
        ),
        (
            # Minimal input for a DNF
            SimpleNamespace(dnf=True),
            ZERO_HF,
        ),
        (
            # DQ and DNF
            SimpleNamespace(dq=True, dnf=True),
            ZERO_HF,
        ),
        (
            SimpleNamespace(
                a=30,
                c=1,
                d=1,
                m=0,
                time=18.7,
                dq=True,
            ),
            ZERO_HF,
        ),
        (
            SimpleNamespace(
                power_factor=PowerFactor.MAJOR,
                a=3,
                c=3,
                m=1,
                ns=1,
                time=3.25,
            ),
            decimal.Decimal("2.1538").quantize(e4),
        ),
        (
            SimpleNamespace(
                power_factor=PowerFactor.MINOR,
                a=3,
                c=3,
                m=1,
                ns=1,
                time=3.25,
            ),
            decimal.Decimal("1.2308").quantize(e4),
        ),
        (
            # Procedural
            SimpleNamespace(
                a=27,
                c=3,
                d=0,
                m=2,
                ns=0,
                procedural=1,
                time=decimal.Decimal("22.14"),
            ),
            decimal.Decimal("5.1491").quantize(e4),
        ),
        (
            SimpleNamespace(
                a=18,
                c=3,
                m=1,
                procedural=0,
                time=decimal.Decimal("26.81"),
            ),
            decimal.Decimal("3.3197").quantize(e4),
        ),
    ]
    VIRGINIA = [
        (
            # Minimal valid input
            SimpleNamespace(
                scoring_type=Scoring.VIRGINIA,
                a=18,
                c=2,
                time=13.21,
            ),
            decimal.Decimal("7.2672").quantize(e4),
        )
    ]
    ALL = CHRONO + FIXED_TIME + COMSTOCK + VIRGINIA
