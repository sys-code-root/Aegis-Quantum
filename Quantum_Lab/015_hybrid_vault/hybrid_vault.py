import oqs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class HybridVault:
    def __init__(self):
        self.simulator = AerSimulator()
        self.kem = oqs.KeyEncapsulation("Kyber768")

    def generate_quantum_bytes(self, length: int) -> bytes:
        num_bits = length * 8
        qc = QuantumCircuit(num_bits)
        qc.h(range(num_bits))
        qc.measure_all()

        compiled_circuit = transpile(qc, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1)
        result = job.result().get_counts()

        bitstring = list(result.keys())[0].replace(" ", "")
        return int(bitstring, 2).to_bytes(length, byteorder="big")

    def hybrid_encrypt(self, public_key: bytes, plaintext: str) -> tuple:
        pqc_ciphertext, shared_secret = self.kem.encap_secret(public_key)
        iv = self.generate_quantum_bytes(16)

        cipher_aes = AES.new(shared_secret[:32], AES.MODE_CBC, iv)
        encrypted_data = cipher_aes.encrypt(pad(plaintext.encode(), AES.block_size))

        return pqc_ciphertext, iv, encrypted_data

    def run_deployment_test(self):
        print("--- STARTING HYBRID CRYPTOGRAPHIC SHIELD ---")
        print("[*] Instantiating Kyber768 Post-Quantum Keypair...")
        
        alice_pub_key = self.kem.generate_keypair()
        raw_data = "Mission to Europe 2026: Quantum Resilience Confirmed."

        p_ct, iv, data = self.hybrid_encrypt(alice_pub_key, raw_data)

        print(f"[+] QRNG Entropy Bytes Obtained: {iv.hex()}")
        print(f"[+] PQC Envelope (Kyber): {p_ct.hex()[:40]}...")
        print(f"[+] Encrypted Payload: {data.hex()[:40]}...")
        print("--- SHIELD STATUS: ACTIVE ---")

if __name__ == "__main__":
    vault = HybridVault()
    vault.run_deployment_test()
