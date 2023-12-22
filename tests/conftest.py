from pathlib import Path
from typing import Callable, Union

import pytest


@pytest.fixture
def mock_data_dir(request: pytest.FixtureRequest) -> Path:
    """Path to root of mock data directory."""
    data_dir = Path(request.config.rootpath) / "tests" / "mock_data"
    assert data_dir.is_dir()
    return data_dir


@pytest.fixture
def mock_data_file(mock_data_dir: Path) -> Callable[[Union[str, Path]], Path]:
    """Provides a function to get the Path to a file in the tests data directory."""

    def get_data_file(filename: str | Path) -> Path:
        fpath = mock_data_dir / filename
        assert fpath.is_file()
        return fpath

    return get_data_file
