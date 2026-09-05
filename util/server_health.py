"""FastAPI server connectivity and health checks for the student client."""

from __future__ import annotations

import json
import socket
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "client_config.json"


def _load_server_url(config_path: str | Path) -> str:
    """Read and validate the FastAPI server URL from the client config."""
    path = Path(config_path)

    with path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    server_url = config.get("server_url")
    if not isinstance(server_url, str) or not server_url.strip():
        raise ValueError(f"Missing or invalid 'server_url' in {path}")

    server_url = server_url.strip().rstrip("/")
    parsed_url = urlparse(server_url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError(f"Invalid server URL in {path}: {server_url!r}")

    return server_url


def check_server_health(
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    timeout: float = 5.0,
) -> dict[str, Any]:
    """Test connectivity to the configured FastAPI ``/health/ready`` endpoint.

    The function does not raise for network or HTTP failures. It returns a
    dictionary containing ``connected``, ``healthy``, ``url``, ``status_code``,
    ``latency_ms``, ``response``, and ``error`` so callers can display a useful
    diagnostic message.
    """
    server_url = _load_server_url(config_path)
    health_url = f"{server_url}/health/ready"
    request = Request(
        health_url,
        headers={"Accept": "application/json", "User-Agent": "course-client/1.0"},
        method="GET",
    )
    started_at = time.perf_counter()

    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = response.status
            content_type = response.headers.get_content_type()
            raw_body = response.read().decode("utf-8", errors="replace")
            body: Any = raw_body

            if content_type == "application/json" and raw_body:
                try:
                    body = json.loads(raw_body)
                except json.JSONDecodeError:
                    pass

            return {
                "connected": True,
                "healthy": 200 <= status_code < 300,
                "url": health_url,
                "status_code": status_code,
                "latency_ms": round((time.perf_counter() - started_at) * 1000, 1),
                "response": body,
                "error": None,
            }
    except HTTPError as error:
        return {
            "connected": True,
            "healthy": False,
            "url": health_url,
            "status_code": error.code,
            "latency_ms": round((time.perf_counter() - started_at) * 1000, 1),
            "response": None,
            "error": f"Server returned HTTP {error.code}: {error.reason}",
        }
    except (URLError, TimeoutError, socket.timeout, OSError) as error:
        reason = error.reason if isinstance(error, URLError) else error
        return {
            "connected": False,
            "healthy": False,
            "url": health_url,
            "status_code": None,
            "latency_ms": round((time.perf_counter() - started_at) * 1000, 1),
            "response": None,
            "error": f"Could not connect to the server: {reason}",
        }


if __name__ == "__main__":
    print(json.dumps(check_server_health(), ensure_ascii=False, indent=2))
