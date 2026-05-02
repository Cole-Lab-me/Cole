"""
Example: Option Strategy Analysis
"""

from option_simulator import StrategyBuilder

print("="*80)
print("OPTION STRATEGY ANALYSIS")
print("="*80)

# Current Market Conditions
spot_price = 100

print(f"\nCurrent Stock Price: ${spot_price}")

# Strategy 1: Long Call
print(f"\n\n{'='*80}")
print("STRATEGY 1: LONG CALL")
print(f"{'='*80}")

print(f"""
Description: Buy a call option
Setup: Buy 1 call at $100 strike for $5 premium

Market View: BULLISH (expect stock to rise)
Max Profit: Unlimited (as stock rises)
Max Loss: Premium paid ($500)
Breakeven: Strike + Premium = $105

Best Used When:
  - You expect stock to rise significantly
  - You want limited downside risk
  - You have moderate confidence in direction
""")

strategy1 = StrategyBuilder.long_call(call_price=5.0, strike=100)
summary1 = strategy1.summary(spot_price)

print(f"Analysis:")
print(f"  Total Cost: ${summary1['total_cost']:.2f}")
print(f"  Max Profit: ${summary1['max_profit']:.2f}")
print(f"  Max Loss: ${summary1['max_loss']:.2f}")
print(f"  Breakeven: ${summary1['breakeven_points']}")

# Profit at different prices
print(f"\nProfit/Loss at Various Stock Prices:")
print(f"{'Stock Price':>12} | {'Payoff':>10} | {'Profit/Loss':>12}")
print("-" * 40)
for spot_test in [80, 90, 100, 105, 110, 120]:
    payoff = strategy1.profit_at_expiration(spot_test)
    print(f"${spot_test:>11} | ${max(0, spot_test - 100):>9.2f} | ${payoff:>11.2f}")

# Strategy 2: Straddle
print(f"\n\n{'='*80}")
print("STRATEGY 2: LONG STRADDLE")
print(f"{'='*80}")

print(f"""
Description: Buy both call and put at same strike
Setup: Buy 1 call at $100 strike for $5 + Buy 1 put at $100 strike for $4

Market View: HIGH VOLATILITY (expect big move either direction)
Max Profit: Unlimited (stock moves far up or down)
Max Loss: Total premium paid ($900)
Breakeven: Strike ± Total Premium = $91 or $109

Best Used When:
  - Major earnings announcement expected
  - Expecting volatile move (direction unknown)
  - Implied volatility is relatively low
  - Before stock splits or major events
""")

strategy2 = StrategyBuilder.straddle(call_price=5.0, put_price=4.0, strike=100)
summary2 = strategy2.summary(spot_price)

print(f"Analysis:")
print(f"  Total Cost: ${summary2['total_cost']:.2f}")
print(f"  Max Profit: ${summary2['max_profit']:.2f}")
print(f"  Max Loss: ${summary2['max_loss']:.2f}")
print(f"  Breakeven Points: ${summary2['breakeven_points']}")

# Profit at different prices
print(f"\nProfit/Loss at Various Stock Prices:")
print(f"{'Stock Price':>12} | {'Call Payoff':>11} | {'Put Payoff':>11} | {'Total P&L':>10}")
print("-" * 50)
for spot_test in [75, 85, 95, 100, 105, 115, 125]:
    payoff = strategy2.profit_at_expiration(spot_test)
    call_val = max(0, spot_test - 100)
    put_val = max(0, 100 - spot_test)
    print(f"${spot_test:>11} | ${call_val:>10.2f} | ${put_val:>10.2f} | ${payoff:>9.2f}")

# Strategy 3: Bull Call Spread
print(f"\n\n{'='*80}")
print("STRATEGY 3: BULL CALL SPREAD")
print(f"{'='*80}")

print(f"""
Description: Buy call at lower strike, sell call at higher strike
Setup: Buy 1 call at $100 strike for $5 + Sell 1 call at $110 strike for $2

Market View: MODERATELY BULLISH (expect stock to rise but limited upside)
Max Profit: Difference in strikes minus net premium = $10 - $3 = $700
Max Loss: Net premium paid ($300)
Breakeven: Lower strike + Net Premium = $103

Best Used When:
  - Expect moderate upside move
  - Want to reduce cost of buying call
  - Want to define maximum profit
  - Neutral on volatility
""")

strategy3 = StrategyBuilder.bull_call_spread(
    long_call_price=5.0,
    short_call_price=2.0,
    long_strike=100,
    short_strike=110
)
summary3 = strategy3.summary(spot_price)

print(f"Analysis:")
print(f"  Total Cost: ${summary3['total_cost']:.2f}")
print(f"  Max Profit: ${summary3['max_profit']:.2f}")
print(f"  Max Loss: ${summary3['max_loss']:.2f}")
print(f"  Breakeven Points: ${summary3['breakeven_points']}")

# Profit at different prices
print(f"\nProfit/Loss at Various Stock Prices:")
print(f"{'Stock Price':>12} | {'Long Call':>11} | {'Short Call':>11} | {'Total P&L':>10}")
print("-" * 50)
for spot_test in [85, 95, 100, 105, 110, 115]:
    long_payoff = max(0, spot_test - 100)
    short_payoff = max(0, spot_test - 110)
    payoff = strategy3.profit_at_expiration(spot_test)
    print(f"${spot_test:>11} | ${long_payoff:>10.2f} | $({short_payoff:>9.2f}) | ${payoff:>9.2f}")

# Strategy 4: Bear Put Spread
print(f"\n\n{'='*80}")
print("STRATEGY 4: BEAR PUT SPREAD")
print(f"{'='*80}")

print(f"""
Description: Sell put at higher strike, buy put at lower strike
Setup: Sell 1 put at $100 strike for $5 + Buy 1 put at $90 strike for $2

Market View: SLIGHTLY BEARISH or NEUTRAL (expect stock to stay above lower strike)
Max Profit: Net credit received ($300)
Max Loss: Difference in strikes minus credit = $10 - $3 = $700
Breakeven: Higher strike - Net Credit = $97

Best Used When:
  - Expect stock to stay above lower strike
  - Want to collect premium (generate income)
  - Neutral to slightly bearish
  - Limited downside risk desired
""")

strategy4 = StrategyBuilder.bear_put_spread(
    long_put_price=2.0,
    short_put_price=5.0,
    long_strike=90,
    short_strike=100
)
summary4 = strategy4.summary(spot_price)

print(f"Analysis:")
print(f"  Total Credit Received: ${-summary4['total_cost']:.2f}")
print(f"  Max Profit: ${summary4['max_profit']:.2f}")
print(f"  Max Loss: ${summary4['max_loss']:.2f}")
print(f"  Breakeven Points: ${summary4['breakeven_points']}")

# Profit at different prices
print(f"\nProfit/Loss at Various Stock Prices:")
print(f"{'Stock Price':>12} | {'Short Put':>11} | {'Long Put':>11} | {'Total P&L':>10}")
print("-" * 50)
for spot_test in [75, 85, 90, 95, 100, 110]:
    short_payoff = max(0, 100 - spot_test)
    long_payoff = max(0, 90 - spot_test)
    payoff = strategy4.profit_at_expiration(spot_test)
    print(f"${spot_test:>11} | $({short_payoff:>9.2f}) | $({long_payoff:>9.2f}) | ${payoff:>9.2f}")

# Strategy Comparison Table
print(f"\n\n{'='*80}")
print("STRATEGY COMPARISON SUMMARY")
print(f"{'='*80}")

print(f"\n{'Strategy':<20} | {'Cost':>10} | {'Max Profit':>12} | {'Max Loss':>12} | {'View':<12}")
print("-" * 75)
print(f"{'Long Call':<20} | ${summary1['total_cost']:>9.2f} | ${summary1['max_profit']:>11.2f} | ${summary1['max_loss']:>11.2f} | {'Bullish':<12}")
print(f"{'Straddle':<20} | ${summary2['total_cost']:>9.2f} | ${summary2['max_profit']:>11.2f} | ${summary2['max_loss']:>11.2f} | {'Vol Play':<12}")
print(f"{'Bull Call Spread':<20} | ${summary3['total_cost']:>9.2f} | ${summary3['max_profit']:>11.2f} | ${summary3['max_loss']:>11.2f} | {'Mod Bull':<12}")
print(f"{'Bear Put Spread':<20} | ${-summary4['total_cost']:>9.2f} | ${summary4['max_profit']:>11.2f} | ${summary4['max_loss']:>11.2f} | {'Income':<12}")

print("\n" + "="*80)
