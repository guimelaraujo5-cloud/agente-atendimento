import unittest

from apps.api.app.core.fsm import ConversationContext, Product, State, advance_state


class FSMTests(unittest.TestCase):
    def test_progression_to_handoff(self):
        ctx = ConversationContext()
        self.assertEqual(advance_state(ctx), State.S1_PRODUCT_SELECT)
        ctx.detected_product = Product.FGTS
        self.assertEqual(advance_state(ctx), State.S2_QUALIFY)
        ctx.qualification_answers = {"saldo_fgts": "sim"}
        self.assertEqual(advance_state(ctx), State.S3_EXPLAIN)
        ctx.consent_given = True
        self.assertEqual(advance_state(ctx), State.S4_CONSENT_AND_MIN_DATA)
        ctx.min_data_complete = True
        self.assertEqual(advance_state(ctx), State.S5_HANDOFF)

    def test_followup_state(self):
        ctx = ConversationContext(inactive_days=3)
        self.assertEqual(advance_state(ctx), State.S6_FOLLOWUP)


if __name__ == "__main__":
    unittest.main()
