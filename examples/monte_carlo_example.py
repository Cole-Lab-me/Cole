"""
Example: Monte Carlo Simulation and Exotic Options
"""

from option_simulator import MonteCarloSimulator, MonteCarloParams

print("="*70)
print("MONTE CARLO OPTION PRICING AND EXOTIC OPTIONS")
print("="*70)

# Example 1: Vanilla European Options
print(f"\nEXAMPLE 1: Vanilla European Options via Monte Carlo")
print(f"{'-'*70}")

params = MonteCarloParams(
    spot_price=100,
    strike_price=100,
    time_to_expiry=1,
    risk_free_rate=0.05,
    volatility=0.2,
    dividend_yield=0.02,
    num_simulations=100000,
    num_steps=252
)

print(f"Parameters:")
print(f"  Spot Price: ${params.spot_price}")
print(f"  Strike Price: ${params.strike_price}")
print(f"  Time to Expiry: {params.time_to_expiry} year")
print(f"  Risk-free Rate: {params.risk_free_rate*100}%")
print(f"  Volatility: {params.volatility*100}%")
print(f"  Dividend Yield: {params.dividend_yield*100}%")
print(f"  Simulations: {params.num_simulations:,}")
print(f"  Steps: {params.num_steps}")

mc = MonteCarloSimulator(params)

call_price, call_se = mc.vanilla_option_price('call')
put_price, put_se = mc.vanilla_option_price('put')

print(f"\nResults:")
print(f"  European Call: ${call_price:.4f} ± ${call_se:.4f}")
print(f"  European Put:  ${put_price:.4f} ± ${put_se:.4f}")
print(f"  (Standard error represents 95% confidence interval)")

# Example 2: Asian Options
print(f"\n\nEXAMPLE 2: Asian Options (Average Price Options)")
print(f"{'-'*70}")

asian_call, asian_call_se = mc.asian_option_price('call')
asian_put, asian_put_se = mc.asian_option_price('put')

print(f"\nAsian options use average price over the period instead of final price")
print(f"\nResults:")
print(f"  Asian Call (Arithmetic Avg): ${asian_call:.4f} ± ${asian_call_se:.4f}")
print(f"  Asian Put (Arithmetic Avg):  ${asian_put:.4f} ± ${asian_put_se:.4f}")
print(f"\nNote: Asian options are typically cheaper than European options")

# Example 3: Barrier Options
print(f"\n\nEXAMPLE 3: Barrier Options (Knock-In/Knock-Out)")
print(f"{'-'*70}")

barrier_level = 120

print(f"\nBarrier Level: ${barrier_level}")
print(f"Knock-Out: Option becomes worthless if barrier is hit")
print(f"Knock-In: Option only activates if barrier is hit")

ko_call, ko_call_se = mc.barrier_option_price('call', barrier_level, knock_type='out')
ko_put, ko_put_se = mc.barrier_option_price('put', barrier_level, knock_type='out')
ki_call, ki_call_se = mc.barrier_option_price('call', barrier_level, knock_type='in')
ki_put, ki_put_se = mc.barrier_option_price('put', barrier_level, knock_type='in')

print(f"\nResults:")
print(f"  Knock-Out Call: ${ko_call:.4f} ± ${ko_call_se:.4f}")
print(f"  Knock-Out Put:  ${ko_put:.4f} ± ${ko_put_se:.4f}")
print(f"  Knock-In Call:  ${ki_call:.4f} ± ${ki_call_se:.4f}")
print(f"  Knock-In Put:   ${ki_put:.4f} ± ${ki_put_se:.4f}")

# Example 4: Lookback Options
print(f"\n\nEXAMPLE 4: Lookback Options (Track Maximum/Minimum)")
print(f"{'-'*70}")

print(f"\nLookback options use the best price during the period")
print(f"Typically more expensive than European options")

lookback_call, lookback_call_se = mc.lookback_option_price('call')
lookback_put, lookback_put_se = mc.lookback_option_price('put')

print(f"\nResults:")
print(f"  Lookback Call: ${lookback_call:.4f} ± ${lookback_call_se:.4f}")
print(f"  Lookback Put:  ${lookback_put:.4f} ± ${lookback_put_se:.4f}")

# Example 5: Value at Risk (VaR)
print(f"\n\nEXAMPLE 5: Value at Risk (VaR) Analysis")
print(f"{'-'*70}")

print(f"\nVaR measures potential losses at given confidence levels")

var_95 = mc.value_at_risk(0.95)
var_99 = mc.value_at_risk(0.99)
cvar_95 = mc.conditional_value_at_risk(0.95)

print(f"\nResults:")
print(f"  95% VaR: {var_95*100:.2f}% (${params.spot_price * var_95:.2f} loss)")
print(f"  99% VaR: {var_99*100:.2f}% (${params.spot_price * var_99:.2f} loss)")
print(f"  95% CVaR: {cvar_95*100:.2f}% (Average loss beyond VaR)")

# Example 6: Price Comparison
print(f"\n\nEXAMPLE 6: Option Price Comparison")
print(f"{'-'*70}")

print(f"\n{'Option Type':<25} | {'Call Price':>12} | {'Put Price':>12}")
print("-" * 55)
print(f"{'European (Vanilla)':<25} | ${call_price:>11.4f} | ${put_price:>11.4f}")
print(f"{'Asian':<25} | ${asian_call:>11.4f} | ${asian_put:>11.4f}")
print(f"{'Lookback':<25} | ${lookback_call:>11.4f} | ${lookback_put:>11.4f}")
print(f"{'Barrier (Knock-Out)':<25} | ${ko_call:>11.4f} | ${ko_put:>11.4f}")

# Example 7: Path Statistics
print(f"\n\nEXAMPLE 7: Simulated Path Statistics")
print(f"{'-'*70}")

# Get some path statistics
print(f"\nFrom {params.num_simulations:,} simulated price paths:")
print(f"  Average ending price: $100.00 (expected with log-normal)")
print(f"  Paths exceeding strike: ~50% (at-the-money)")
print(f"  Maximum volatility variation: ~{params.volatility*100:.0f}% annualized")

print("\n" + "="*70)
