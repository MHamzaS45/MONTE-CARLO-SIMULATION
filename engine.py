import numpy as np
from models.gbm import GeometricBrownianMotion
from analytics.diagnostics import confidence_interval


class MonteCarloEngine:
    def __init__(self, market, simulation):
        self.market = market
        self.simulation = simulation

        np.random.seed(self.simulation.seed)

        self.model = GeometricBrownianMotion(
            market.spot,
            market.rate,
            market.volatility,
        )

    def price(self, option_type: str = "call"):
        paths = self.model.simulate_paths(
            self.market.maturity,
            n_steps=252,
            n_paths=self.simulation.n_paths,
        )

        terminal = paths[:, -1]

        if option_type == "call":
            payoffs = np.maximum(terminal - self.market.strike, 0.0)
        elif option_type == "put":
            payoffs = np.maximum(self.market.strike - terminal, 0.0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

        discounted = np.exp(-self.market.rate * self.market.maturity) * payoffs

        price = np.mean(discounted)
        std = np.std(discounted)

        ci_half_width = 1.96 * std / np.sqrt(len(discounted))
        ci = (price - ci_half_width, price + ci_half_width)

        return price, ci, discounted