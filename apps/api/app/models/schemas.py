from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Literal, Optional


@dataclass
class LeadUpdate:
    status: Literal["new", "qualified", "waiting_data", "handoff_sent", "closed"]
    customer_preference: Literal["menor_parcela", "maior_valor", "mais_rapido", "nao_informado"]


@dataclass
class LLMResponse:
    reply_text: str
    detected_product: str
    state: str
    fields_to_capture: List[str]
    lead_update: LeadUpdate
    qualification_answers: Dict[str, Optional[str]]
    handoff_ready: bool
    handoff_payload: Optional[dict] = None

    @classmethod
    def model_validate(cls, payload: dict) -> "LLMResponse":
        required = [
            "reply_text",
            "detected_product",
            "state",
            "fields_to_capture",
            "lead_update",
            "qualification_answers",
            "handoff_ready",
            "handoff_payload",
        ]
        missing = [k for k in required if k not in payload]
        if missing:
            raise ValueError(f"Missing keys: {missing}")
        lead_update = LeadUpdate(**payload["lead_update"])
        return cls(
            reply_text=payload["reply_text"],
            detected_product=payload["detected_product"],
            state=payload["state"],
            fields_to_capture=payload["fields_to_capture"],
            lead_update=lead_update,
            qualification_answers=payload["qualification_answers"],
            handoff_ready=payload["handoff_ready"],
            handoff_payload=payload["handoff_payload"],
        )


@dataclass
class LeadHandoff:
    id: str
    channel: Literal["whatsapp", "instagram"]
    user_id: str
    conversation_id: str
    product: Literal["INSS", "FGTS", "CLT", "CARTAO", "AUXILIO_BRASIL"]
    name: str
    cpf: str
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    nis_number: Optional[str] = None
    benefit_amount: Optional[float] = None
    company_name: Optional[str] = None
    card_bank: Optional[str] = None
    preferred_installments: Optional[int] = None
    qualification_answers: Optional[dict] = None
    customer_preference: str = "nao_informado"
    status: str = "new"
    next_action: str = "simulate"
    notes: str = ""
