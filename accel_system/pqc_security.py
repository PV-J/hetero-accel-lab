# accel_system/pqc_security.py

import hashlib
import os
from typing import Tuple

class PQCSecurityAccelerator:
    """
    Toy post-quantum cryptography accelerator model.

    This DOES NOT implement real PQC.
    It just mimics:
      - keypair()
      - encapsulate()
      - decapsulate()
    with a simple latency model.
    """

    def __init__(self, name: str = "pqc_accel",
                 keygen_latency: float = 0.2, # was 2.0
                 encap_latency: float = 0.1, # was 1.5
                 decap_latency: float = 0.1, # was 1.5
        ):
        self.name = name
        self.keygen_latency = keygen_latency
        self.encap_latency = encap_latency
        self.decap_latency = decap_latency

    # ---- toy primitives ----

    def _toy_hash(self, data: bytes) -> bytes:
        return hashlib.sha256(data).digest()

    # ---- public API ----

    def keypair(self) -> Tuple[bytes, bytes, float]:
        """Return (public_key, secret_key, latency)."""
        sk = os.urandom(32)
        pk = self._toy_hash(sk)
        return pk, sk, self.keygen_latency

    def encapsulate(self, pk: bytes, plaintext: bytes) -> Tuple[bytes, bytes, float]:
        """
        Toy 'encapsulation':
          shared_secret = H(pk || plaintext)
          ciphertext    = plaintext XOR H(shared_secret)
        """
        shared_secret = self._toy_hash(pk)
        mask = self._toy_hash(shared_secret)

        # XOR plaintext with mask (truncate mask as needed)
        mask_stream = (mask * ((len(plaintext) // len(mask)) + 1))[: len(plaintext)]
        ciphertext = bytes(p ^ m for p, m in zip(plaintext, mask_stream))

        return ciphertext, shared_secret, self.encap_latency

    def decapsulate(self, pk: bytes, sk: bytes, ciphertext: bytes) -> Tuple[bytes, bytes, float]:
        """
        Toy 'decapsulation': recompute shared_secret and recover plaintext.
        Here we do something symmetric just so example runs.
        """
        # For a toy example, pretend shared_secret depends only on sk.
        shared_secret = self._toy_hash(pk)
        mask = self._toy_hash(shared_secret)
        mask_stream = (mask * ((len(ciphertext) // len(mask)) + 1))[: len(ciphertext)]
        plaintext = bytes(c ^ m for c, m in zip(ciphertext, mask_stream))

        return plaintext, shared_secret, self.decap_latency
