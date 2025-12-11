# accel_system/dsp_accel.py

from typing import List, Tuple

class DSPAccelerator:
    """
    Toy DSP accelerator that applies a simple moving-average filter.
    """

    def __init__(self, name: str = "dsp_accel", base_latency: float = 0.5):
        self.name = name
        self.base_latency = base_latency

    def run(self, signal: List[float], window: int = 3) -> Tuple[List[float], float]:
        if not signal or window <= 1:
            return signal, self.base_latency

        out = []
        n = len(signal)
        for i in range(n):
            start = max(0, i - window + 1)
            window_vals = signal[start : i + 1]
            out.append(sum(window_vals) / len(window_vals))

        # toy latency: base + cost proportional to samples * window
        ops = n * window
        latency = self.base_latency + 0.0005 * ops
        return out, latency
