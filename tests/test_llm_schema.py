import json
import unittest

from apps.api.app.services.llm_orchestrator import LLMOrchestrator


class LLMSchemaTests(unittest.TestCase):
    def test_valid_json_schema(self):
        payload = {
            "reply_text": "Oi!",
            "detected_product": "INSS",
            "state": "S2_QUALIFY",
            "fields_to_capture": ["name"],
            "lead_update": {
                "status": "new",
                "customer_preference": "nao_informado"
            },
            "qualification_answers": {"recebe_inss": "sim"},
            "handoff_ready": False,
            "handoff_payload": None
        }
        orchestrator = LLMOrchestrator()
        model = orchestrator.validate_response(json.dumps(payload))
        self.assertEqual(model.detected_product, "INSS")


if __name__ == "__main__":
    unittest.main()
