import json
import os
from datetime import datetime

class TransactionStore:
    def __init__(self, file_path="app/db/transactions.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def log_transaction(self, transaction_type: str, data: dict):
        """Log a transaction with timestamp"""
        transaction = {
            "id": f"{transaction_type}_{int(datetime.now().timestamp())}",
            "type": transaction_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        transactions = self.get_all_transactions()
        transactions.append(transaction)

        with open(self.file_path, "w") as file:
            json.dump(transactions, file, indent=2)

        return transaction

    def get_all_transactions(self):
        """Get all logged transactions"""
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_transaction(self, transaction_id: str):
        """Get a specific transaction by ID"""
        transactions = self.get_all_transactions()
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                return transaction
        return None

transaction_store = TransactionStore()