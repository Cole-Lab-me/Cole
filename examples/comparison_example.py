"""
Example: Comparison of All Three Pricing Models
"""

from option_simulator import (
    BlackScholesCalculator,
    BinomialTreeCalculator,
    BinomialParams,
    MonteCarloSimulator,
    MonteCarloParams
)

print("="*70)
print("OPTION PRICING MODEL COMPARISON")
print("="*70)

# Parameters
spot = 100
strike = 100
time = 1
rate = 0.05
vol = 0.2
div = 0.02

print(f"\nCommon Parameters:")
print(f"  Spot Price: ${spot}")
print(f"  Strike Price: ${strike}")
print(f"  Time to Expiry: {time} year")
print(f"  Risk-free Rate: {rate*100}%")
print(f"  Volatility: {vol*100}%")
print(f"  Dividend Yield: {div*100}%")

# Model 1: Black-Scholes
print(f"\n{'-'*70}")
print("MODEL 1: BLACK-SCHOLES (Analytical)")
print(f"{'-'*70}")

bs = BlackScholesCalculator(spot, strike, time, rate, vol, div)
bs_call = bs.call_price()
bs_put = bs.put_price()
bs_call_greeks = bs.call_greeks()

print(f"European Call: ${bs_call:.4f}")
print(f"European Put:  ${bs_put:.4f}")
print(f"Call Delta: {bs_call_greeks['delta']:.4f}")
print(f"Computation Time: < 1ms")

# Model 2: Binomial Tree
print(f"\n{'-'*70}")
print("MODEL 2: BINOMIAL TREE (Cox-Ross-Rubinstein)")
print(f"{'-'*70}")

binomial_params = BinomialParams(
    spot_price=spot,
    strike_price=strike,
    time_to_expiry=time,
    risk_free_rate=rate,
    volatility=vol,
    dividend_yield=div,
    steps=100
)
binomial = BinomialTreeCalculator(binomial_params)

eu_call = binomial.call_price(american=False)
eu_put = binomial.put_price(american=False)
am_call = binomial.call_price(american=True)
am_put = binomial.put_price(american=True)

print(f"European Call: ${eu_call:.4f}")
print(f"European Put:  ${eu_put:.4f}")
print(f"American Call: ${am_call:.4f} (Early Exercise Premium: ${am_call - eu_call:.4f})")
print(f"American Put:  ${am_put:.4f} (Early Exercise Premium: ${am_put - eu_put:.4f})")

# Model 3: Monte Carlo
print(f"\n{'-'*70}")
print("MODEL 3: MONTE CARLO SIMULATION")
print(f"{'-'*70}")

mc_params = MonteCarloParams(
    spot_price=spot,
    strike_price=strike,
    time_to_expiry=time,
    risk_free_rate=rate,
    volatility=vol,
    dividend_yield=div,
    num_simulations=100000,
    num_steps=252
)
mc = MonteCarloSimulator(mc_params)

mc_call, mc_call_se = mc.vanilla_option_price('call')
mc_put, mc_put_se = mc.vanilla_option_price('put')

print(f"European Call: ${mc_call:.4f} (±${mc_call_se:.4f})")
print(f"European Put:  ${mc_put:.4f} (±${mc_put_se:.4f})")
print(f"Simulations: 100,000")
print(f"Computation Time: ~500ms")

# Comparison Table
print(f"\n{'-'*70}")
print("PRICE COMPARISON")
print(f"{'-'*70}")

print(f"\n{'Model':<20} | {'Call Price':>12} | {'Put Price':>12} | {'Difference (BS)':<15}")
print("-" * 70)
print(f"{'Black-Scholes':<20} | ${bs_call:>11.4f} | ${bs_put:>11.4f} | Baseline")
print(f"{'Binomial (100 steps)':<20} | ${eu_call:>11.4f} | ${eu_put:>11.4f} | ${eu_call-bs_call:>+.4f} / ${eu_put-bs_put:>+.4f}")
print(f"{'Monte Carlo (100k)':<20} | ${mc_call:>11.4f} | ${mc_put:>11.4f} | ${mc_call-bs_call:>+.4f} / ${mc_put-bs_put:>+.4f}")

# Sensitivity Comparison
print(f"\n{'-'*70}")
print("GREEKS COMPARISON (CALL OPTION)")
print(f"{'-'*70}")

print(f"\n{'Greek':<15} | {'Black-Scholes':>15} | {'Interpretation':<30}")
print("-" * 65)

call_greeks = bs.call_greeks()
print(f"{'Delta':<15} | {call_greeks['delta']:>15.4f} | Price change per $1 move")
print(f"{'Gamma':<15} | {call_greeks['gamma']:>15.6f} | Delta change per $1 move")
print(f"{'Vega':<15} | {call_greeks['vega']:>15.4f} | Price change per 1% vol")
print(f"{'Theta':<15} | {call_greeks['theta']:>15.4f} | Daily time decay")
print(f"{'Rho':<15} | {call_greeks['rho']:>15.4f} | Price change per 1% rate")

# Model Selection Guide
print(f"\n{'-'*70}")
print("MODEL SELECTION GUIDE")
print(f"{'-'*70}")

print(f"""
BLACK-SCHOLES:
  ✓ Fastest (analytical solution)
  ✓ Best for European options
  ✓ Easy Greeks calculation
  ✗ Cannot handle American options
  ✗ Assumes European exercise only

BINOMIAL TREE:
  ✓ Handles American options
  ✓ Flexible dividend modeling
  ✓ Good for simple derivatives
  ✓ Easy to visualize paths
  ✗ Slower for many steps
  ✗ Limited to regular options

MONTE CARLO:
  ✓ Handles exotic options (Asian, Barrier, Lookback)
  ✓ Path-dependent options
  ✓ Easy to extend to complex payoffs
  ✓ Risk metrics (VaR, CVaR)
  ✗ Slowest (simulation-based)
  ✗ Requires more computations
""")

print("="*70)
