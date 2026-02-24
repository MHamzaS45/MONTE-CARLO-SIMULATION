"""
Finite Difference Delta
"""

def delta(engine, epsilon: float = 1e-4) -> float:
    original_spot = engine.market.spot

    engine.market.spot = original_spot + epsilon
    price_up, _, _ = engine.price()

    engine.market.spot = original_spot - epsilon
    price_down, _, _ = engine.price()

    engine.market.spot = original_spot

    return (price_up - price_down) / (2 * epsilon)