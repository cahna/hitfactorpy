import functools
from decimal import Decimal


def DecimalQ(q: str, v) -> Decimal:
    return Decimal(v).quantize(Decimal(q))


D2 = functools.partial(DecimalQ, "0.01")
D4 = functools.partial(DecimalQ, "0.0001")
