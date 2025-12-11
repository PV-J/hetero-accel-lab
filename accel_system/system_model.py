# accel_system/system_model.py
# SystemModel takes matrix_size and dsp_window and can generate a toy matrix/vector for that size
# This kind of parameterized system model is common in accelerator evaluation work

from typing import List, Dict, Any
import random

from .matrix_accel import MatrixAccelerator
from .pqc_security import PQCSecurityAccelerator
from .dsp_accel import DSPAccelerator
from .scheduler import SimpleScheduler
from .rf_radio import RFModule



class SystemModel:
    """
    Pipeline:
      input -> MatrixAccelerator -> DSPAccelerator -> PQCSecurityAccelerator
    """

    def __init__(self, matrix_size: int = 3, dsp_window: int = 3, seed: int = 0, rf_bandwidth_mbps: float = 10.0,):
        self.matrix_accel = MatrixAccelerator()
        self.dsp_accel = DSPAccelerator()
        self.pqc_accel = PQCSecurityAccelerator()
        self.scheduler = SimpleScheduler()
        self.rf_module = RFModule()
        self.matrix_size = matrix_size
        self.dsp_window = dsp_window
        self.seed = seed
        self.rf_module = RFModule(bandwidth_mbps=rf_bandwidth_mbps)

    def make_input(self) -> (List[List[float]], List[float]):
        """Create a random matrix/vector of configured size."""
        random.seed(self.seed)
        n = self.matrix_size
        matrix = [[random.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]
        vector = [random.uniform(-1.0, 1.0) for _ in range(n)]
        return matrix, vector

    def run_pipeline(self, matrix: List[List[float]], vector: List[float]) -> Dict[str, Any]:
        y, mat_lat = self.matrix_accel.run(matrix, vector)

        dsp_out, dsp_lat = self.dsp_accel.run(y, window=self.dsp_window)

        # serialize DSP output and send over RF link
        dsp_bytes = ",".join(f"{v:.4f}" for v in dsp_out).encode("utf-8")
        rf_payload, rf_lat = self.rf_module.transmit(dsp_bytes)

        pk, sk, keygen_lat = self.pqc_accel.keypair()
        ct, ss_enc, enc_lat = self.pqc_accel.encapsulate(pk, rf_payload)
        pt, ss_dec, dec_lat = self.pqc_accel.decapsulate(pk, sk, ct)

        total_latency = mat_lat + dsp_lat + rf_lat + keygen_lat + enc_lat + dec_lat

        latencies = {
            "matrix": mat_lat,
            "dsp": dsp_lat,
            "rf": rf_lat,
            "pqc_keygen": keygen_lat,
            "pqc_encapsulate": enc_lat,
            "pqc_decapsulate": dec_lat,
            "total": total_latency,
        }

        bottleneck_stage, bottleneck_latency = self.scheduler.find_bottleneck(latencies)

        return {
            "matrix_output": y,
            "dsp_output": dsp_out,
            "plaintext_bytes_recovered": pt,
            "shared_secret_match": (ss_enc == ss_dec),
            "latencies": latencies,
            "bottleneck": {
                "stage": bottleneck_stage,
                "latency": bottleneck_latency,
            },
        }
