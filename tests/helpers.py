from httpx import Response


def get_json(resp: Response, status_code=200) -> dict:
    assert (
        resp.status_code == status_code
    ), f"Unexpected response: {resp.status_code} {resp.text}"
    return resp.json()
