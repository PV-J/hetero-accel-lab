# accel_system/scheduler.py

from typing import Dict, Tuple


class SimpleScheduler:
    """
    Tiny helper that inspects the latency breakdown and labels the bottleneck.

    It does NOT change execution order yet; it just analyzes results.
    """

    def find_bottleneck(self, latencies: Dict[str, float]) -> Tuple[str, float]:
        """
        Given a dict of {stage_name: latency}, return (bottleneck_stage, latency),
        ignoring the aggregate 'total' entry if present.
        """
        filtered = {k: v for k, v in latencies.items() if k != "total"}
        if not filtered:
            return "none", 0.0

        # max by latency
        stage = max(filtered, key=lambda k: filtered[k])
        return stage, filtered[stage]
