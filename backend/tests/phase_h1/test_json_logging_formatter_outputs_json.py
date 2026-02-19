import json
import logging
from app.core.logging_config import configure_json_logging


def test_json_logging_formatter_outputs_json(capfd):
    configure_json_logging(level="INFO")
    logging.getLogger("test").info("hello ops")

    out = capfd.readouterr().out.strip()
    payload = json.loads(out)

    assert payload["level"] == "INFO"
    assert payload["logger"] == "test"
    assert payload["message"] == "hello ops"

