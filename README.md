# Monte Carlo Pricer Engine

A small, modular Monte Carlo simulation project for **pricing European options** under a **Geometric Brownian Motion (GBM)** model. The repository includes a pricing engine with a 95% confidence interval, a Black–Scholes benchmark for validation, convergence diagnostics, and a finite-difference Delta example.

## Scope and capabilities

- **Products**: European call and put options (plain-vanilla payoff at maturity)
- **Model**: GBM with constant drift/volatility
- **Outputs**:
  - Monte Carlo price estimate
  - 95% confidence interval (normal approximation)
  - Discounted payoff samples (useful for diagnostics)
  - Optional convergence plot vs. Black–Scholes price
- **Sensitivity example**: Delta via central finite differences

## Repository structure

```text
Monte-Carlo-Simulation/
├── analytics/
│   ├── black_scholes.py        # closed-form European call (benchmark)
│   └── diagnostics.py          # confidence interval + convergence plot
├── models/
│   └── gbm.py                  # GBM path simulator
├── variance/
│   └── antithetic.py           # antithetic normal generator (not wired by default)
├── config.py                   # MarketParams / SimulationParams dataclasses
├── engine.py                   # MonteCarloEngine (pricing + CI)
├── greeks.py                   # finite-difference Delta
├── main.py                     # runnable example (prints results + plot)
├── Monte Carlo simulation.py   # legacy single-file baseline script
├── requirements.txt
└── README.md
```

## Installation

### Requirements

- Python 3.x
- Required packages listed in `requirements.txt`:
  - `numpy`
  - `scipy`
  - `matplotlib`

### Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Quick start

Run the example entry point:

```powershell
python .\main.py
```

This will:

- price a European call via Monte Carlo
- print the estimate and 95% confidence interval
- compute the Black–Scholes call price (benchmark)
- compute Delta using finite differences
- display a convergence plot of the running Monte Carlo mean vs. Black–Scholes

## How it works

### Configuration

Market and simulation inputs are defined in `config.py`:

- `MarketParams(spot, strike, rate, volatility, maturity)`
- `SimulationParams(n_paths, seed=42, antithetic=True)`

### Pricing engine

`engine.py` defines `MonteCarloEngine`, which:

- seeds NumPy’s RNG using `SimulationParams.seed`
- simulates GBM paths using `models/gbm.py`
- computes terminal payoffs for `"call"` or `"put"`
- discounts payoffs with \(e^{-rT}\)
- returns `(price, ci, discounted_payoffs)`

The engine uses a fixed **252 time steps** per path (trading-day convention).

### GBM simulation

`models/gbm.py` simulates paths in log space using per-step normal increments:

\[
\log S_{t+\Delta t} - \log S_t = (r - \tfrac{1}{2}\sigma^2)\Delta t + \sigma\sqrt{\Delta t}\,Z
\]

This yields lognormal paths consistent with GBM under constant parameters.

## Using the engine in your own script

Create market/simulation parameters, instantiate the engine, and price:

```python
from config import MarketParams, SimulationParams
from engine import MonteCarloEngine

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
price, ci, discounted = engine.price("call")  # or "put"
print(price, ci, discounted.shape)
```

## Notes and limitations

- The included Black–Scholes function (`analytics/black_scholes.py`) benchmarks a **European call** only.
- Confidence intervals use a normal approximation with a fixed 1.96 z-score for 95% confidence.
- The variance reduction helper in `variance/antithetic.py` is provided, but **not connected** to `MonteCarloEngine` by default.

