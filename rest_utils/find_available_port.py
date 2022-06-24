import socket
from typing import Optional, cast

def find_available_port() -> int:
    """Finds a local random unoccupied TCP port.
    Returns:
        A random unoccupied TCP port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        _, port = s.getsockname()

    return cast(int, port)

find_available_port()