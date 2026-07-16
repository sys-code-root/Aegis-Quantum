import hashlib
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QuantumHashLedger:
    def __init__(self):
        self.simulator = AerSimulator()
        self.blockchain = []

    def _generate_quantum_bit(self) -> int:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()

        compiled_qc = transpile(qc, self.simulator)
        job = self.simulator.run(compiled_qc, shots=1)
        counts = job.result().get_counts()
        
        if not counts:
            return 0
        return int(list(counts.keys())[0])

    def _generate_quantum_bytes(self, num_bytes: int = 32) -> bytes:
        byte_list = []
        for _ in range(num_bytes):
            byte_value = 0
            for bit_position in range(8):
                byte_value |= (self._generate_quantum_bit() << bit_position)
            byte_list.append(byte_value)
        return bytes(byte_list)

    def generate_lamport_keypair(self) -> tuple:
        secret_key_0 = [self._generate_quantum_bytes(32) for _ in range(256)]
        secret_key_1 = [self._generate_quantum_bytes(32) for _ in range(256)]

        public_key_0 = [hashlib.sha256(x).digest() for x in secret_key_0]
        public_key_1 = [hashlib.sha256(x).digest() for x in secret_key_1]

        return (secret_key_0, secret_key_1), (public_key_0, public_key_1)

    def sign_transaction(self, message: str, secret_key: tuple) -> list:
        message_hash = hashlib.sha256(message.encode()).digest()
        signature = []

        for byte in message_hash:
            for bit_position in range(8):
                bit = (byte >> bit_position) & 1
                index = len(signature)

                if bit == 0:
                    signature.append(secret_key[0][index])
                else:
                    signature.append(secret_key[1][index])
        return signature

    def verify_signature(self, message: str, signature: list, public_key: tuple) -> bool:
        message_hash = hashlib.sha256(message.encode()).digest()

        for i, byte in enumerate(message_hash):
            for bit_position in range(8):
                bit = (byte >> bit_position) & 1
                index = i * 8 + bit_position

                if index >= len(signature):
                    return False

                sig_hash = hashlib.sha256(signature[index]).digest()
                expected_pub = public_key[0][index] if bit == 0 else public_key[1][index]

                if sig_hash != expected_pub:
                    return False
        return True

    def add_block(self, transaction_data: str):
        print(f"[*] Processing ledger transaction input: '{transaction_data}'")

        sk, pk = self.generate_lamport_keypair()

        sig = self.sign_transaction(transaction_data, sk)

        if self.verify_signature(transaction_data, sig, pk):
            self.blockchain.append({"data": transaction_data, "signature": sig})
            print("[+] STATUS: Transaction block verified and securely committed to the ledger.")
        else:
            print("[-] ALERT: Cryptographic identity validation failed. Transaction rejected.")

if __name__ == "__main__":
    ledger = QuantumHashLedger()
    print("--- QUANTUM-RESISTANT HASH LEDGER ---")

    ledger.add_block("TX_FROM:Alice_TX_TO:Bob_AMOUNT:10_BTC")
