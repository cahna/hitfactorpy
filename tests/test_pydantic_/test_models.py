import pytest

from hitfactorpy.pydantic_.models import UspsaStageScore

from ..parametrize.hit_factor import HitFactorTestCases


@pytest.mark.parametrize("test_input,expected", HitFactorTestCases.ALL)
def test_valid_UspsaStageScore(test_input, expected):
    assert UspsaStageScore(**vars(test_input)).calculate_hit_factor() == expected
