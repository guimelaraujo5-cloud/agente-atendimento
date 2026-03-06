from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional


class State(str, Enum):
    S0_GREETING = "S0_GREETING"
    S1_PRODUCT_SELECT = "S1_PRODUCT_SELECT"
    S2_QUALIFY = "S2_QUALIFY"
    S3_EXPLAIN = "S3_EXPLAIN"
    S4_CONSENT_AND_MIN_DATA = "S4_CONSENT_AND_MIN_DATA"
    S5_HANDOFF = "S5_HANDOFF"
    S6_FOLLOWUP = "S6_FOLLOWUP"


class Product(str, Enum):
    INSS = "INSS"
    FGTS = "FGTS"
    CLT = "CLT"
    CARTAO = "CARTAO"
    AUXILIO_BRASIL = "AUXILIO_BRASIL"
    UNKNOWN = "UNKNOWN"


@dataclass
class ConversationContext:
    state: State = State.S0_GREETING
    detected_product: Product = Product.UNKNOWN
    qualification_answers: Dict[str, Optional[str]] = field(default_factory=dict)
    consent_given: bool = False
    min_data_complete: bool = False
    inactive_days: int = 0


def advance_state(ctx: ConversationContext) -> State:
    if ctx.inactive_days in {1, 3, 7}:
        ctx.state = State.S6_FOLLOWUP
        return ctx.state

    if ctx.state == State.S0_GREETING:
        ctx.state = State.S1_PRODUCT_SELECT
    elif ctx.state == State.S1_PRODUCT_SELECT and ctx.detected_product != Product.UNKNOWN:
        ctx.state = State.S2_QUALIFY
    elif ctx.state == State.S2_QUALIFY and _is_qualified(ctx):
        ctx.state = State.S3_EXPLAIN
    elif ctx.state == State.S3_EXPLAIN and ctx.consent_given:
        ctx.state = State.S4_CONSENT_AND_MIN_DATA
    elif ctx.state == State.S4_CONSENT_AND_MIN_DATA and ctx.min_data_complete:
        ctx.state = State.S5_HANDOFF
    return ctx.state


def _is_qualified(ctx: ConversationContext) -> bool:
    if ctx.detected_product == Product.UNKNOWN:
        return False
    return any(v not in (None, "", "nao") for v in ctx.qualification_answers.values())
