import json
from datetime import datetime
from pathlib import Path

TRANSACTIONS_FILE = Path(__file__).parent / "transactions.json"

def save_transaction(record: dict):
    record["timestamp"] = datetime.utcnow().isoformat()
    
    transactions = []
    if TRANSACTIONS_FILE.exists():
        try:
            with open(TRANSACTIONS_FILE) as f:
                content = f.read().strip()
                if content:
                    transactions = json.loads(content)
        except (json.JSONDecodeError, Exception):
            transactions = []
    
    transactions.append(record)
    
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(transactions, f, indent=2)

def list_transactions():
    if not TRANSACTIONS_FILE.exists():
        return []
    
    try:
        with open(TRANSACTIONS_FILE) as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, Exception):
        return []

transaction_store = type('TransactionStore', (), {
    'log_transaction': lambda self, t, d: save_transaction({**d, 'type': t})
})()