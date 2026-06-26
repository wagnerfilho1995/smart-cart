import logging


class EndpointFilter(logging.Filter):
    """Filter class to exclude specific endpoints from log entries."""

    def __init__(self, excluded_endpoints: list[str]) -> None:
        self.excluded_endpoints = excluded_endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        return not (
            record.args
            and len(record.args) >= 5
            and record.args[2] in self.excluded_endpoints
            and record.args[4] == 200
        )
