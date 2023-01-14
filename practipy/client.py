from typing import Optional

import httpx

_PRACTIPY_CACHE_DIR = "../../.practipy_cache"


def get_match_report(match_id: Optional[str] = None):
    """WIP"""
    if match_id:
        match_url = f"https://practiscore.com/reports/web/{match_id}"
        response = httpx.get(match_url)
        return response.text

    # for development
    with open(f"{_PRACTIPY_CACHE_DIR}/reports/match__01e65294-8692-4adf-9897-29dc01a68360.txt", "r") as f:
        return f.read()
