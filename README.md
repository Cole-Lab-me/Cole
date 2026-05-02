# Option Pricing Simulator

A comprehensive financial options pricing simulator supporting multiple pricing models and strategies.

## Features

- **Black-Scholes Model**: European option pricing with Greeks calculation
- **Binomial Model**: American and European option pricing
- **Monte Carlo Simulation**: Path-dependent option pricing
- **Greeks Calculation**: Delta, Gamma, Vega, Theta, Rho
- **Strategy Analysis**: Multi-leg option strategies
- **Interactive Dashboard**: Real-time pricing visualization
- **Portfolio Analysis**: Multiple position management

## Installation

```bash
git clone https://github.com/Cole-Lab-me/Cole.git
cd Cole
pip install -r requirements.txt
```

## Quick Start

```python
from option_simulator import BlackScholesCalculator

# Create calculator
calc = BlackScholesCalculator(
    spot_price=100,
    strike_price=100,
    time_to_expiry=1,
    risk_free_rate=0.05,
    volatility=0.2
)

# Calculate call option price
call_price = calc.call_price()
call_greeks = calc.call_greeks()

print(f"Call Price: ${call_price:.2f}")
print(f"Delta: {call_greeks['delta']:.4f}")
print(f"Gamma: {call_greeks['gamma']:.4f}")
print(f"Vega: {call_greeks['vega']:.4f}")
```

## Usage

### Command Line Interface

```bash
# Calculate single option
python -m option_simulator --model black-scholes --spot 100 --strike 100 --rate 0.05 --volatility 0.2 --time 1

# Run interactive dashboard
python -m option_simulator --dashboard
```

### Python API

See `examples/` directory for comprehensive examples.

## Pricing Models

### 1. Black-Scholes
Best for: European options, quick calculations
- Closed-form solution
- Fast computation
- Greeks calculation

### 2. Binomial Tree
Best for: American options, dividends, discrete events
- Flexible dividend handling
- American exercise support
- Path visualization

### 3. Monte Carlo
Best for: Complex derivatives, path dependencies
- Exotic options support
- Convergence analysis
- Sensitivity analysis

## Documentation

- [Models](docs/models.md)
- [API Reference](docs/api.md)
- [Examples](examples/)
- [Strategy Guide](docs/strategies.md)

## License

MIT
