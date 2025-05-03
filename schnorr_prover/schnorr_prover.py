# File: schnorr_prover.py
from ecdsa import SECP256k1, ellipticcurve
from hashlib import sha256
import random

# Initialize elliptic curve parameters (secp256k1)
curve = SECP256k1.curve
G = SECP256k1.generator
n = SECP256k1.order


class Prover:
    def __init__(self):
        self.x = random.randint(1, n - 1)  # Private key
        self.y = self.x * G  # Public key

    def generate_proof(self):
        # Generate random nonce k and commitment R
        k = random.randint(1, n - 1)
        R = k * G

        # Compute challenge c via Fiat-Shamir (hash R and public key y)
        c = self._hash_points(R, self.y)

        # Calculate response s = k + c*x
        s = (k + c * self.x) % n
        return (R, s)

    def _hash_points(self, R, y):
        # Serialize point coordinates and hash
        data = f"{R.x()},{R.y()},{y.x()},{y.y()}"
        return int(sha256(data.encode()).hexdigest(), 16) % n


class Verifier:
    def __init__(self, y):
        self.y = y

    def verify_proof(self, R, s):
        # Recompute challenge c
        c = self._hash_points(R, self.y)

        # Verify equation: s*G == R + c*y
        left = s * G
        right = R + c * self.y
        return left == right

    def _hash_points(self, R, y):
        # Consistent hashing logic with the Prover
        data = f"{R.x()},{R.y()},{y.x()},{y.y()}"
        return int(sha256(data.encode()).hexdigest(), 16) % n


# Example execution
if __name__ == "__main__":
    prover = Prover()
    R, s = prover.generate_proof()
    verifier = Verifier(prover.y)
    is_valid = verifier.verify_proof(R, s)
    print(f"Proof Validity: {is_valid}")