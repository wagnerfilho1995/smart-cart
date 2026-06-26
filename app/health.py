from fastapi_health import health


def test_application_ready() -> bool:
    return True


api_health = health([test_application_ready])
