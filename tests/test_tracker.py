from sdk.api_tracker.tracker import Tracker


class DummyTransport:
    def __init__(self):
        self.sent = []

    def send_usage(self, usage):
        self.sent.append(usage)
        return True


def test_tracker_records_usage(monkeypatch):
    tracker = Tracker(project="demo", provider="openai")
    dummy = DummyTransport()
    tracker.transport = dummy

    usage = tracker.record(
        model="gpt-5", input_tokens=10, output_tokens=5, total_tokens=15
    )

    assert usage.total_tokens == 15
    assert dummy.sent[0]["model"] == "gpt-5"


def test_transport_failure_does_not_raise(monkeypatch):
    tracker = Tracker(project="demo", provider="openai")

    class FailingTransport:
        def send_usage(self, usage):
            raise RuntimeError("boom")

    tracker.transport = FailingTransport()

    usage = tracker.record(model="gpt-5")
    assert usage.model == "gpt-5"
