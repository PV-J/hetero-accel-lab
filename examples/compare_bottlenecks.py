# examples/compare_bottlenecks.py

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from accel_system.system_model import SystemModel


def run_case(matrix_size, dsp_window, rf_bandwidth_mbps, label):
    system = SystemModel(
        matrix_size=matrix_size,
        dsp_window=dsp_window,
        seed=0,
        rf_bandwidth_mbps=rf_bandwidth_mbps,
    )
    matrix, vector = system.make_input()
    result = system.run_pipeline(matrix, vector)

    print(f"\n=== {label} ===")
    print(f"matrix_size={matrix_size}, dsp_window={dsp_window}, rf_bandwidth={rf_bandwidth_mbps} Mb/s")
    for k, v in result["latencies"].items():
        print(f"  {k:>16}: {v:.4f}")
    print("  bottleneck:", result["bottleneck"]["stage"])


def main():
    # Compute-heavy bottleneck
    run_case(matrix_size=32, dsp_window=3, rf_bandwidth_mbps=100.0, label="Compute-heavy")

    # Communication-heavy bottleneck
    run_case(matrix_size=32, dsp_window=3, rf_bandwidth_mbps=0.01, label="Communication-heavy")


if __name__ == "__main__":
    main()
