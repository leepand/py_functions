import socket


def get_free_port():
    try:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("localhost", 0))
        (hostname, port) = s.getsockname()
        s.close()
        return (hostname, port)
    except socket.error:
        return (None, None)


get_free_port()
