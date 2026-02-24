import numpy as np


class GeometricBrownianMotion:
    def __init__(self, spot, rate, volatility):
        self.spot = spot
        self.rate = rate
        self.volatility = volatility

    def simulate_paths(self, maturity, n_steps, n_paths):
        dt = maturity / n_steps

        drift = (self.rate - 0.5 * self.volatility**2) * dt
        diffusion = self.volatility * np.sqrt(dt)

        z = np.random.standard_normal((n_paths, n_steps))
        increments = drift + diffusion * z

        log_paths = np.cumsum(increments, axis=1)
        S = self.spot * np.exp(log_paths)

        return np.column_stack([np.full(n_paths, self.spot), S])