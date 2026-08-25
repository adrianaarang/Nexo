"""Sincronización del modo offline (Equipo 4, siguiente prioridad).

Router mínimo de la base común. TODO (Equipo 4): recibir las acciones
guardadas offline por el frontend (ver
frontend/js/siguiente/modo-offline/syncQueue.js) y aplicarlas sobre los
modelos de cada módulo (necesidades, voluntariado, donaciones, personas).
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
import sqlite3
from sync.services import process_sync_batch

router = APIRouter(prefix="/api/sync", tags=["sync"])

# TODO: @router.post("")

def get_db():
    conn = sqlite3.connect("nexo.db")
    try:
        yield conn
    finally:
        conn.close()

router = APIRouter(prefix="/api/sync", tags=["Offline Sync"])

# Request Schema Contract
class SyncOperation(BaseModel):
    operation_id: str
    entity_type: str
    entity_id: str
    operation_type: str
    payload: Dict[str, Any]
    client_created_at: str

class SyncBatchRequest(BaseModel):
    operations: List[SyncOperation]

# Response Schema Contract
class SyncResult(BaseModel):
    operation_id: str
    status: str

class SyncBatchResponse(BaseModel):
    results: List[SyncResult]

@router.post("/batch", response_model=SyncBatchResponse)
def sync_offline_batch(request: SyncBatchRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Receives a batch of offline operations from the frontend, 
    processes them transactionally, and returns the deterministic status of each.
    """
    try:
        # Convert Pydantic models to dicts for our service function
        operations_dict_list = [op.model_dump() for op in request.operations]
        
        # Process the batch using our tested Phase 4 service
        results = process_sync_batch(db, operations_dict_list)
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Catastrophic sync failure: {str(e)}")
