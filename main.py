from config import MarketParams, SimulationParams
from engine import MonteCarloEngine
from analytics.black_scholes import black_scholes_call
from analytics.diagnostics import plot_convergence
from greeks import delta as finite_delta


def main():
    market = MarketParams(
        spot=100,
        strike=105,
        rate=0.05,
        volatility=0.2,
        maturity=1.0,
    )

    simulation = SimulationParams(
        n_paths=100_000,
        seed=42,
        antithetic=True,
    )

    engine = MonteCarloEngine(market, simulation)

    mc_price, ci, discounted = engine.price("call")

    bs_price = black_scholes_call(
        market.spot,
        market.strike,
        market.rate,
        market.volatility,
        market.maturity,
    )

    delta = finite_delta(engine)

    print("========== Monte Carlo European Call ==========")
    print(f"Monte Carlo Price: {mc_price:.6f}")
    print(f"95% CI: [{ci[0]:.6f}, {ci[1]:.6f}]")
    print(f"Black-Scholes Price: {bs_price:.6f}")
    print(f"Absolute Error: {abs(mc_price - bs_price):.6f}")
    print(f"Delta: {delta:.6f}")

    plot_convergence(discounted, bs_price)


if __name__ == "__main__":
    main()