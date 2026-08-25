"""
Data structures and database helpers for sync operations.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
import json


class OperationType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class SyncStatus(str, Enum):
    PENDING = "PENDING"
    APPLIED = "APPLIED"
    ALREADY_APPLIED = "ALREADY_APPLIED"
    CONFLICT = "CONFLICT"
    INVALID = "INVALID"
    RETRYABLE_ERROR = "RETRYABLE_ERROR"


@dataclass
class SyncOperationRecord:
    operation_id: str
    entity_type: str
    entity_id: str
    operation_type: OperationType
    status: SyncStatus
    payload: Dict[str, Any]
    client_created_at: str
    id: Optional[int] = None
    server_processed_at: Optional[datetime] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "operation_type": self.operation_type.value,
            "status": self.status.value,
            "payload": self.payload,
            "client_created_at": self.client_created_at,
            "server_processed_at": self.server_processed_at.isoformat() if self.server_processed_at else None,
            "error_code": self.error_code,
            "error_message": self.error_message,
        }