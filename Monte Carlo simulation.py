###########################################################
# Monte Carlo Simulation for European Option Pricing 
# Project done by : Hamza Sahqani
 ###########################################################


import numpy as np

# Setting stock price & simulation parameters
S0 = 100      # Initial stock price
K = 105       # Strike price
T = 1.0       # Time to maturity
r = 0.05      # Risk-free rate
sigma = 0.2   # Volatility
N = 100000    # Number of simulations

# Enumerate the steps of the Monte Carlo Simulation
z = np.random.standard_normal(N)                                                  
ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
payoffs = np.maximum(ST - K, 0)
option_price = np.exp(-r * T) * np.mean(payoffs)

print(f"Option Price: {option_price:.4f}")
