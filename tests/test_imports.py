import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from cyberai import ai, security


def test_modules_importable():
    assert callable(ai.analyze)
    assert callable(security.ingest_event)
