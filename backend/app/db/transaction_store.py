import json
from datetime import datetime
from pathlib import Path

TRANSACTIONS_FILE = Path(__file__).parent / "transactions.json"

def save_transaction(record: dict):
    record["timestamp"] = datetime.utcnow().isoformat()
    
    transactions = []
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE) as f:
            transactions = json.load(f)
    
    transactions.append(record)
    
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(transactions, f, indent=2)

def list_transactions():
    if not TRANSACTIONS_FILE.exists():
        return []
    
    with open(TRANSACTIONS_FILE) as f:
        return json.load(f)

transaction_store = type('TransactionStore', (), {
    'log_transaction': lambda self, t, d: save_transaction({**d, 'type': t})
})()