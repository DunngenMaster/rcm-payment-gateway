import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.db.models.transaction_log import TransactionLog


class TransactionStore:
    """Store transaction logs in MySQL"""

    def log_transaction(self, transaction_type: str, transaction_data: dict, merchant_id: str = None):
        """Log a transaction to the database"""
        db: Session = SessionLocal()
        try:
            # Extract merchant_id from data if not provided
            if not merchant_id:
                merchant_id = transaction_data.get("merchant_id")
            
            if not merchant_id:
                raise ValueError("merchant_id is required for logging transactions")

            # Create transaction log entry
            log_entry = TransactionLog(
                merchant_id=merchant_id,
                type=transaction_type,
                status=transaction_data.get("status", "completed"),
                amount=transaction_data.get("amount"),
                order_id=transaction_data.get("order_id"),
                clover_reference_id=transaction_data.get("clover_reference_id"),
                response_payload=json.dumps(transaction_data.get("payload", {})) if transaction_data.get("payload") else None,
            )
            db.add(log_entry)
            db.commit()
        finally:
            db.close()

    def list_transactions(self, merchant_id: str = None, transaction_type: str = None) -> list:
        """List transactions from database"""
        db: Session = SessionLocal()
        try:
            query = db.query(TransactionLog)
            
            if merchant_id:
                query = query.filter_by(merchant_id=merchant_id)
            if transaction_type:
                query = query.filter_by(type=transaction_type)
            
            transactions = query.order_by(TransactionLog.timestamp.desc()).all()
            
            # Convert to dict format for backwards compatibility
            return [
                {
                    "id": t.id,
                    "merchant_id": t.merchant_id,
                    "type": t.type,
                    "status": t.status,
                    "amount": t.amount,
                    "order_id": t.order_id,
                    "clover_reference_id": t.clover_reference_id,
                    "payload": json.loads(t.response_payload) if t.response_payload else {},
                    "timestamp": t.timestamp.isoformat(),
                }
                for t in transactions
            ]
        finally:
            db.close()

    def get_transaction(self, transaction_id: str) -> dict | None:
        """Get a single transaction by ID"""
        db: Session = SessionLocal()
        try:
            t = db.query(TransactionLog).filter_by(id=transaction_id).first()
            if not t:
                return None
            return {
                "id": t.id,
                "merchant_id": t.merchant_id,
                "type": t.type,
                "status": t.status,
                "amount": t.amount,
                "order_id": t.order_id,
                "clover_reference_id": t.clover_reference_id,
                "payload": json.loads(t.response_payload) if t.response_payload else {},
                "timestamp": t.timestamp.isoformat(),
            }
        finally:
            db.close()


def save_transaction(record: dict):
    """Legacy function for backwards compatibility"""
    store = TransactionStore()
    store.log_transaction(
        transaction_type=record.get("type", "unknown"),
        transaction_data=record,
        merchant_id=record.get("merchant_id"),
    )


def list_transactions(merchant_id: str = None):
    """Legacy function for backwards compatibility"""
    store = TransactionStore()
    return store.list_transactions(merchant_id=merchant_id)


transaction_store = TransactionStore()
