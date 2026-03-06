from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="guimel-assist", version="0.2.0")

# MVP in-memory store (substituir por repositórios PostgreSQL em produção)
DB: Dict[str, Dict[str, Any]] = {
    "leads": {},
    "conversations": {},
    "handoffs": {},
    "metrics": {
        "messages_inbound": 0,
        "messages_outbound": 0,
        "leads_total": 0,
    },
}


class MessageSendRequest(BaseModel):
    channel: str
    user_id: str
    message_text: str
    conversation_id: Optional[str] = None


class LeadPatchStatus(BaseModel):
    status: str


class LeadAssign(BaseModel):
    assigned_to: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "guimel-assist", "timestamp": datetime.utcnow().isoformat()}


@app.post("/webhooks/whatsapp")
def whatsapp_webhook(payload: dict) -> dict:
    DB["metrics"]["messages_inbound"] += 1
    return {"received": True, "channel": "whatsapp", "payload_echo": payload}


@app.get("/webhooks/whatsapp/verify")
def whatsapp_verify() -> dict:
    return {"verify": "ok", "provider": "meta_whatsapp"}


@app.post("/webhooks/instagram")
def instagram_webhook(payload: dict) -> dict:
    DB["metrics"]["messages_inbound"] += 1
    return {"received": True, "channel": "instagram", "payload_echo": payload}


@app.get("/webhooks/instagram/verify")
def instagram_verify() -> dict:
    return {"verify": "ok", "provider": "meta_instagram"}


@app.post("/messages/send")
def send_message(req: MessageSendRequest) -> dict:
    DB["metrics"]["messages_outbound"] += 1
    conv_id = req.conversation_id or str(uuid4())
    DB["conversations"].setdefault(conv_id, {"messages": []})
    DB["conversations"][conv_id]["messages"].append(
        {"direction": "outbound", "text": req.message_text, "at": datetime.utcnow().isoformat()}
    )
    return {"sent": True, "conversation_id": conv_id}


@app.post("/messages/send/batch")
def send_message_batch(payload: List[MessageSendRequest]) -> dict:
    ids = []
    for req in payload:
        res = send_message(req)
        ids.append(res["conversation_id"])
    return {"sent": len(payload), "conversation_ids": ids}


@app.get("/admin/leads")
def admin_list_leads() -> dict:
    return {"items": list(DB["leads"].values()), "total": len(DB["leads"])}


@app.get("/admin/leads/{lead_id}")
def admin_lead_detail(lead_id: str) -> dict:
    lead = DB["leads"].get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return lead


@app.patch("/admin/leads/{lead_id}/status")
def admin_patch_status(lead_id: str, body: LeadPatchStatus) -> dict:
    lead = DB["leads"].get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    lead["status"] = body.status
    lead["updated_at"] = datetime.utcnow().isoformat()
    return lead


@app.patch("/admin/leads/{lead_id}/assign")
def admin_assign(lead_id: str, body: LeadAssign) -> dict:
    lead = DB["leads"].get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    lead["assigned_to"] = body.assigned_to
    lead["updated_at"] = datetime.utcnow().isoformat()
    return lead


@app.post("/admin/handoffs/{handoff_id}/export")
def admin_export_handoff(handoff_id: str) -> dict:
    handoff = DB["handoffs"].get(handoff_id)
    if not handoff:
        raise HTTPException(status_code=404, detail="Handoff não encontrado")
    return {"exported": True, "handoff": handoff}


@app.get("/admin/conversations/{conversation_id}")
def admin_conversation_detail(conversation_id: str) -> dict:
    conv = DB["conversations"].get(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return conv


@app.get("/admin/metrics")
def admin_metrics() -> dict:
    return DB["metrics"]


@app.delete("/privacy/user/{user_id}")
def privacy_delete_user(user_id: str) -> dict:
    # MVP: apenas confirmação. Produção: anonimizar em todas as tabelas relacionadas.
    return {"deleted_or_anonymized": True, "user_id": user_id}


@app.post("/privacy/export/{user_id}")
def privacy_export_user(user_id: str) -> dict:
    return {"user_id": user_id, "export": "pending_generation"}
