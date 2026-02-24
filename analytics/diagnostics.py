import numpy as np
import matplotlib.pyplot as plt


def confidence_interval(values: np.ndarray, confidence: float = 0.95):
    mean = np.mean(values)
    std = np.std(values)

    z = 1.96  # Approx for 95% confidence
    half_width = z * std / np.sqrt(len(values))

    return mean, (mean - half_width, mean + half_width)


def plot_convergence(discounted_payoffs: np.ndarray, bs_price: float):
    running_mean = np.cumsum(discounted_payoffs) / np.arange(1, len(discounted_payoffs) + 1)

    plt.figure()
    plt.plot(running_mean)
    plt.axhline(bs_price, linestyle="--")
    plt.title("Monte Carlo Convergence")
    plt.xlabel("Simulations")
    plt.ylabel("Price")
    plt.show()