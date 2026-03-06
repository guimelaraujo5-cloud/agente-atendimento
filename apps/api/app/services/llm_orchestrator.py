import json
from typing import Any, Dict

from apps.api.app.models.schemas import LLMResponse


SYSTEM_PROMPT = """Você é o Assistente Guimel, atendente comercial especializado.
Atende WhatsApp e Instagram com mensagens curtas e humanas.
Faz no máximo 1 pergunta por mensagem.
Primeiro entende a intenção; depois identifica o produto.
Aplica triagem e explica o produto de forma simples.
Nunca promete aprovação/liberação/taxa fixa.
Nunca pede senhas, códigos, gov.br, token, CVV.
Não pede fotos de documentos/cartão no atendimento inicial.
Pede dados mínimos para simulação somente com consentimento.
Sempre tenta converter para simulação ou agendar retorno.
Sempre encerra com próximo passo claro.
Deve responder em JSON estruturado, nunca texto livre."""


class LLMOrchestrator:
    def build_context(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "state": conversation.get("state"),
            "recent_messages": conversation.get("recent_messages", [])[-8:],
            "detected_product": conversation.get("detected_product", "UNKNOWN"),
            "collected_fields": conversation.get("collected_fields", {}),
        }

    def validate_response(self, raw_text: str) -> LLMResponse:
        payload = json.loads(raw_text)
        return LLMResponse.model_validate(payload)

    def safe_fallback(self) -> Dict[str, Any]:
        return {
            "reply_text": "Perfeito! Posso te ajudar com uma simulação rápida. Você prefere INSS, FGTS, CLT, Cartão ou Bolsa Família?",
            "detected_product": "UNKNOWN",
            "state": "S1_PRODUCT_SELECT",
            "fields_to_capture": [],
            "lead_update": {
                "status": "new",
                "customer_preference": "nao_informado",
            },
            "qualification_answers": {},
            "handoff_ready": False,
            "handoff_payload": None,
        }
