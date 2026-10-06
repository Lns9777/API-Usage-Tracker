import socket

from backend.app.launcher import find_available_port


def test_find_available_port_skips_busy_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as busy_socket:
        busy_socket.bind(("127.0.0.1", 0))
        busy_port = busy_socket.getsockname()[1]

        selected_port = find_available_port("127.0.0.1", busy_port)

    assert selected_port != busy_port
