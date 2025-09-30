import pytest

from app import clients


class _Capture:
    def __init__(self):
        self.calls = []


def test_fetch_topics_calls_expected_url(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "t1", "name": "Topic 1"}]
    
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_topics()
    
    assert response == [{"id": "t1", "name": "Topic 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/topics")
