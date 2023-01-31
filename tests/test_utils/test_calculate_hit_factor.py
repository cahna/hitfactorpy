import pytest

from hitfactorpy.utils import calculate_hit_factor

from ..parametrize.hit_factor import HitFactorTestCases


@pytest.mark.parametrize("test_input,expected", HitFactorTestCases.CHRONO)
def test_calculate_hit_factor_chrono(test_input, expected):
    assert calculate_hit_factor(**vars(test_input)) == expected


@pytest.mark.parametrize("test_input,expected", HitFactorTestCases.COMSTOCK)
def test_calculate_hit_factor_comstock(test_input, expected):
    assert calculate_hit_factor(**vars(test_input)) == expected


@pytest.mark.parametrize("test_input,expected", HitFactorTestCases.VIRGINIA)
def test_calculate_hit_factor_virginia(test_input, expected):
    assert calculate_hit_factor(**vars(test_input)) == expected


@pytest.mark.parametrize("test_input,expected", HitFactorTestCases.FIXED_TIME)
def test_calculate_hit_factor_fixed_time(test_input, expected):
    assert calculate_hit_factor(**vars(test_input)) == expected
