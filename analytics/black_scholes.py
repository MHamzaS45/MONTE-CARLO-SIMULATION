import numpy as np
from scipy.stats import norm


def black_scholes_call(spot, strike, rate, vol, maturity) -> float:
    d1 = (np.log(spot / strike) + (rate + 0.5 * vol**2) * maturity) / (vol * np.sqrt(maturity))
    d2 = d1 - vol * np.sqrt(maturity)

    return (
        spot * norm.cdf(d1)
        - strike * np.exp(-rate * maturity) * norm.cdf(d2)
    )