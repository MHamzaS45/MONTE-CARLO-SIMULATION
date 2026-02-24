from dataclasses import dataclass


@dataclass
class MarketParams:
    spot: float
    strike: float
    rate: float
    volatility: float
    maturity: float


@dataclass
class SimulationParams:
    n_paths: int
    seed: int = 42
    antithetic: bool = True