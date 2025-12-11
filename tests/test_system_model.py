import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from accel_system.system_model import SystemModel


def test_shared_secret_matches():
    system = SystemModel()
    matrix = [
        [1.0, 0.5],
        [0.0, 1.0],
    ]
    vector = [1.0, 2.0]

    result = system.run_pipeline(matrix, vector)
    assert result["shared_secret_match"]
    assert "total" in result["latencies"]
