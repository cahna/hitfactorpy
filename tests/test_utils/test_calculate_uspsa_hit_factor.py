import decimal
from types import SimpleNamespace

import pytest

from hitfactorpy.enums import PowerFactor, Scoring
from hitfactorpy.utils import calculate_uspsa_hit_factor

e4 = decimal.Decimal("0.0001")
ZERO_HF = decimal.Decimal().quantize(e4)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            # Minimal valid input
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type="chrono"),
                hit_factor=0,
            ),
            decimal.Decimal().quantize(e4),
        ),
        (
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type="chrono"),
                hit_factor=6.1234,
            ),
            decimal.Decimal("6.1234").quantize(e4),
        ),
        (
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type="chrono"),
                hit_factor=6.12340000,
            ),
            decimal.Decimal("6.1234").quantize(e4),
        ),
        (
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type="chrono"),
                hit_factor=6.123400001,
            ),
            decimal.Decimal("6.1234").quantize(e4),
        ),
    ],
)
def test_calculate_uspsa_hit_factor_chrono(test_input, expected):
    assert calculate_uspsa_hit_factor(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            # Minimal valid input
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=None),
                competitor=SimpleNamespace(power_factor=PowerFactor.MINOR),
                a=30,
                c=1,
                d=1,
                m=0,
                ns=0,
                time=18.7,
            ),
            decimal.Decimal("8.2353").quantize(e4),
        ),
        (
            # Same score, but major power factor
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=None),
                competitor=SimpleNamespace(power_factor=PowerFactor.MAJOR),
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
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=None),
                dq=True,
                dnf=False,
            ),
            ZERO_HF,
        ),
        (
            # Minimal input for a DNF
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=None),
                dq=False,
                dnf=True,
            ),
            ZERO_HF,
        ),
        (
            # DQ and DNF
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=Scoring.COMSTOCK),
                dq=True,
                dnf=True,
            ),
            ZERO_HF,
        ),
        (
            # Competitor DQ
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=Scoring.COMSTOCK),
                competitor=SimpleNamespace(dq=True),
                a=30,
                c=1,
                d=1,
                m=0,
                ns=0,
                time=18.7,
            ),
            ZERO_HF,
        ),
        (
            # stage_power_factor overrides competitor.power_factor
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=Scoring.COMSTOCK),
                competitor=SimpleNamespace(power_factor=PowerFactor.MAJOR),
                stage_power_factor=PowerFactor.MINOR,
                a=3,
                c=3,
                d=0,
                m=1,
                ns=1,
                time=3.25,
            ),
            decimal.Decimal("1.2308").quantize(e4),
        ),
        (
            # Procedural
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=Scoring.COMSTOCK),
                competitor=SimpleNamespace(power_factor=PowerFactor.MINOR),
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
    ],
)
def test_calculate_uspsa_hit_factor_comstock(test_input, expected):
    assert calculate_uspsa_hit_factor(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            # Minimal valid input
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=Scoring.VIRGINIA),
                competitor=SimpleNamespace(power_factor=PowerFactor.MINOR),
                a=18,
                c=2,
                d=0,
                m=0,
                ns=0,
                time=13.21,
            ),
            decimal.Decimal("7.2672").quantize(e4),
        ),
    ],
)
def test_calculate_uspsa_hit_factor_virginia(test_input, expected):
    assert calculate_uspsa_hit_factor(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            # Minimal valid input
            SimpleNamespace(
                stage=SimpleNamespace(scoring_type=Scoring.FIXED_TIME),
                competitor=SimpleNamespace(power_factor=PowerFactor.MINOR),
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
                stage=SimpleNamespace(scoring_type=Scoring.FIXED_TIME),
                competitor=SimpleNamespace(power_factor=PowerFactor.MAJOR),
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
                stage=SimpleNamespace(scoring_type=Scoring.FIXED_TIME),
                competitor=SimpleNamespace(power_factor=PowerFactor.MAJOR),
                stage_power_factor=PowerFactor.MINOR,
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
                stage=SimpleNamespace(scoring_type=Scoring.FIXED_TIME),
                competitor=SimpleNamespace(power_factor=PowerFactor.MINOR),
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
    ],
)
def test_calculate_uspsa_hit_factor_fixed_time(test_input, expected):
    assert calculate_uspsa_hit_factor(test_input) == expected
