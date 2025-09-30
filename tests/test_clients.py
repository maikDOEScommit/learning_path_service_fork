import pytest
from app import clients


# Hilfsklasse, um Aufrufe und übergebene Daten abzufangen
class _Capture:
    def __init__(self):
        self.calls = []   # speichert URLs, die aufgerufen wurden
        self.args = []    # speichert die übergebenen Daten (Payloads)
        self.kwargs = []  # könnte für optionale Parameter genutzt werden


# Test: fetch_topics ruft die richtige URL auf und gibt das Ergebnis zurück
def test_fetch_topics_calls_expected_url(monkeypatch):
    cap = _Capture()

    # Mock ersetzt clients.get_json durch diese Funktion
    def mock_get_json(url):
        cap.calls.append(url)  # merke dir, welche URL aufgerufen wird
        return [{"id": "t1", "name": "Topic 1"}]  # simuliere API-Response

    # Patch: ersetze get_json in clients durch unsere Fake-Version
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    # Aufruf der Funktion, die wir testen wollen
    response = clients.fetch_topics()

    # Überprüfe Rückgabewert und Nebenwirkungen
    assert response == [{"id": "t1", "name": "Topic 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/topics")  # URL muss auf /topics enden


# Test: fetch_topic ruft die Detail-URL mit Topic-ID auf
def test_fetch_topic_by_id(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return {"id": "t2", "name": "Topic 2"}

    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_topic("t2")

    assert response["id"] == "t2"
    assert "/topics/t2" in cap.calls[0]  # richtige URL mit ID


# Test: create_topic sendet POST mit korrekten Daten
def test_create_topic_posts_correct_data(monkeypatch):
    cap = _Capture()

    def mock_post_json(url, data):
        cap.calls.append(url)
        cap.args.append(data)
        return {"id": "t3", "name": data["name"]}

    monkeypatch.setattr(clients, "post_json", mock_post_json)

    response = clients.create_topic({"name": "New Topic"})

    assert response["id"] == "t3"
    assert cap.calls[0].endswith("/topics")
    assert cap.args[0] == {"name": "New Topic"}  # Payload stimmt


# Test: update_topic ruft PUT mit korrekten Daten auf
def test_update_topic_puts_expected_data(monkeypatch):
    cap = _Capture()

    def mock_put_json(url, data):
        cap.calls.append(url)
        cap.args.append(data)
        return {"id": "t4", "name": data["name"]}

    monkeypatch.setattr(clients, "put_json", mock_put_json)

    response = clients.update_topic("t4", {"name": "Updated"})

    assert response["id"] == "t4"
    assert cap.calls[0].endswith("/topics/t4")
    assert cap.args[0] == {"name": "Updated"}


# Test: delete_topic ruft DELETE auf der richtigen URL
def test_delete_topic_calls_delete(monkeypatch):
    cap = _Capture()

    def mock_delete(url):
        cap.calls.append(url)
        return {"deleted": True}

    monkeypatch.setattr(clients, "delete", mock_delete)

    response = clients.delete_topic("t5")

    assert response == {"deleted": True}
    assert cap.calls[0].endswith("/topics/t5")
