# examples/example_inference_with_pqc.py
# Add CLI options to the example to parse --matrix-size and --dsp-window
# Command‑line configuration like this is a lightweight way to explore design space for hardware models

import os
import sys
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from accel_system.system_model import SystemModel


def parse_args():
    parser = argparse.ArgumentParser(description="hetero-accel-lab matrix + DSP + RF + PQC example")
    parser.add_argument("--matrix-size", type=int, default=3, help="square matrix size N (N x N)")
    parser.add_argument("--dsp-window", type=int, default=3, help="DSP moving-average window")
    parser.add_argument("--rf-bandwidth-mbps", type=float, default=10.0, help="RF link bandwidth in Mb/s")
    parser.add_argument("--seed", type=int, default=0, help="random seed for input generation")
    return parser.parse_args()


def main():
    args = parse_args()

    system = SystemModel(
        matrix_size=args.matrix_size,
        dsp_window=args.dsp_window,
        seed=args.seed,
        rf_bandwidth_mbps=args.rf_bandwidth_mbps,
    )

    matrix, vector = system.make_input()
    result = system.run_pipeline(matrix, vector)

    print("=== hetero-accel-lab: matrix + DSP + PQC example ===")
    print(f"Matrix size: {args.matrix_size}x{args.matrix_size}")
    print(f"DSP window: {args.dsp_window}")
    print(f"RF bandwidth: {args.rf_bandwidth_mbps} Mb/s")
    print("Matrix output:", result["matrix_output"])
    print("DSP output:", result["dsp_output"])
    print("Shared secret match:", result["shared_secret_match"])
    print("Latency breakdown (time units):")
    for k, v in result["latencies"].items():
        print(f"  {k:>16}: {v:.4f}")

    print("Bottleneck stage:", result["bottleneck"]["stage"])
    print("Bottleneck latency:", f'{result["bottleneck"]["latency"]:.4f}')


if __name__ == "__main__":
    main()
