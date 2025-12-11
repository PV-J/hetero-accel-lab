# accel_system/rf_radio.py

from typing import List, Tuple


class RFModule:
    """
    Toy RF/wireless link model with:
      - fixed propagation latency
      - serialization latency based on bandwidth
    """

    def __init__(
        self,
        name: str = "rf_module",
        propagation_latency: float = 2.0,  # was 0.5 base link delay
        bandwidth_mbps: float = 10.0,      # data rate in megabits/s
    ):
        self.name = name
        self.propagation_latency = propagation_latency
        self.bandwidth_mbps = bandwidth_mbps

    def transmit(self, payload: bytes) -> Tuple[bytes, float]:
        """
        Returns (received_payload, latency).

        Latency = propagation + serialization_time,
        where serialization_time = payload_bits / bandwidth.
        """
        bits = len(payload) * 8
        # convert Mb/s to b/s: bandwidth_mbps * 1e6
        serialization_time = bits / (self.bandwidth_mbps * 1e6)
        latency = self.propagation_latency + serialization_time
        return payload, latency
