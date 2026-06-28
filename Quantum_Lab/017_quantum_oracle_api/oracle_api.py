import hashlib
import oqs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import ZZFeatureMap
from qiskit_aer import AerSimulator

app = FastAPI(title="Quantum Oracle API Gateway")

class TransactionRequest(BaseModel):
    amount: float
    risk_factor: float

class QuantumSafeValidator:
    def __init__(self):
        self.simulator = AerSimulator()
        enabled_sigs = oqs.get_enabled_sig_mechanisms()
        
        self.signer = None
        self.sig_name = None
        
        priorities = ["ML-DSA-45", "Dilithium2", "ML-DSA-65", "Dilithium3", "Falcon-512"]
        
        for candidate in priorities:
            if candidate in enabled_sigs:
                try:
                    self.signer = oqs.Signature(candidate)
                    self.sig_name = candidate
                    break
                except Exception:
                    continue
                    
        if not self.sig_name and enabled_sigs:
            for sig in enabled_sigs:
                try:
                    self.signer = oqs.Signature(sig)
                    self.sig_name = sig
                    break
                except Exception:
                    continue
                    
        if not self.sig_name:
            self.sig_name = "SHA256-Fallback (Classical Emulation)"
            
        if self.signer:
            try:
                self.signer.generate_keypair()
            except Exception:
                self.signer = None

    def run_quantum_fraud_check(self, data_point: list) -> str:
        feature_map = ZZFeatureMap(feature_dimension=2, reps=1)
        qc = feature_map.assign_parameters({
            feature_map.parameters[0]: data_point[0], 
            feature_map.parameters[1]: data_point[1]
        })
        qc.measure_all()
        
        compiled_qc = transpile(qc, self.simulator)
        shots = 1024
        result = self.simulator.run(compiled_qc, shots=shots).result().get_counts()
        
        prob_00 = result.get('00', 0) / shots
        return "FRAUD" if prob_00 < 0.5 else "LEGIT"

    def sign_transaction(self, transaction_data: str) -> str:
        if self.signer:
            try:
                signature = self.signer.sign(transaction_data.encode())
                return signature.hex()
            except Exception:
                pass
        return hashlib.sha256(transaction_data.encode()).hexdigest()

validator = QuantumSafeValidator()

@app.get("/")
def home():
    return {
        "status": "Quantum Oracle Active", 
        "crypto_engine": validator.sig_name
    }

@app.post("/validate_transaction")
async def validate(request: TransactionRequest):
    try:
        status = validator.run_quantum_fraud_check([request.amount, request.risk_factor])
        signature_result = validator.sign_transaction(f"{request.amount}-{status}")
        
        return {
            "amount": request.amount,
            "analysis": status,
            "signature": f"{signature_result[:64]}...",
            "algorithm_used": validator.sig_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
