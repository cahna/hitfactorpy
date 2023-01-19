import httpx

_hitfactorpy_CACHE_DIR = "../../.hitfactorpy_cache"
_test_match_id = "01e65294-8692-4adf-9897-29dc01a68360"


def get_cached_report(cache_dir: str = _hitfactorpy_CACHE_DIR, match_id: str = _test_match_id):
    with open(f"{cache_dir}/reports/match__{match_id}.txt", "r") as f:
        return f.read()


def get_match_report(match_id: str = _test_match_id):
    """WIP"""
    if match_id and match_id is not _test_match_id:
        match_url = f"https://practiscore.com/reports/web/{match_id}"
        response = httpx.get(match_url)
        return response.text

    # for development
    get_cached_report(match_id)
