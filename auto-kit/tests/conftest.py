import socket
import pytest

@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError('테스트의 실제 외부 연결 금지')
    monkeypatch.setattr(socket.socket, 'connect', blocked)
