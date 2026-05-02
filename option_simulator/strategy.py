"""
Option Strategy Analyzer
Implements common option strategies: straddle, strangle, spread, collar, etc.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum


class StrategyType(Enum):
    """Common option strategies"""
    CALL = "call"
    PUT = "put"
    STRADDLE = "straddle"  # Long call + long put at same strike
    STRANGLE = "strangle"  # Long call + long put at different strikes
    BULL_CALL_SPREAD = "bull_call_spread"  # Long call + short call higher strike
    BEAR_PUT_SPREAD = "bear_put_spread"  # Long put + short put lower strike
    COLLAR = "collar"  # Long stock + long put + short call
    BUTTERFLY = "butterfly"  # Long 1 call, short 2 calls, long 1 call


@dataclass
class Leg:
    """Single leg of an option strategy"""
    option_type: str  # 'call' or 'put'
    strike: float
    price: float
    quantity: int = 1
    premium_paid: bool = True  # True if buying, False if selling


class OptionStrategy:
    """Option strategy analyzer"""
    
    def __init__(self, name: str, legs: List[Leg]):
        self.name = name
        self.legs = legs
    
    def total_cost(self) -> float:
        """Calculate total cost/credit of strategy"""
        cost = 0
        for leg in self.legs:
            if leg.premium_paid:
                cost += leg.price * leg.quantity * 100  # Contract is for 100 shares
            else:
                cost -= leg.price * leg.quantity * 100  # Credit received
        return cost
    
    def max_profit(self, spot_price: float) -> float:
        """Calculate maximum possible profit"""
        # Need to evaluate at various spot prices
        max_profit = float('-inf')
        
        for test_price in self._get_test_prices(spot_price):
            profit = self.profit_at_expiration(test_price)
            max_profit = max(max_profit, profit)
        
        return max_profit
    
    def max_loss(self, spot_price: float) -> float:
        """Calculate maximum possible loss"""
        min_profit = float('inf')
        
        for test_price in self._get_test_prices(spot_price):
            profit = self.profit_at_expiration(test_price)
            min_profit = min(min_profit, profit)
        
        return min_profit
    
    def profit_at_expiration(self, spot_price: float) -> float:
        """Calculate profit/loss at a specific spot price"""
        profit = -self.total_cost()
        
        for leg in self.legs:
            if leg.option_type == 'call':
                payoff = max(spot_price - leg.strike, 0)
            else:  # put
                payoff = max(leg.strike - spot_price, 0)
            
            payoff *= 100  # Standard contract size
            
            if leg.premium_paid:
                profit += payoff * leg.quantity
            else:
                profit -= payoff * leg.quantity
        
        return profit
    
    def breakeven_points(self, spot_price: float) -> List[float]:
        """Calculate breakeven price(s)"""
        breakevens = []
        prices = self._get_test_prices(spot_price, granularity=0.5)
        
        previous_profit = None
        previous_price = None
        
        for price in prices:
            profit = self.profit_at_expiration(price)
            
            if previous_profit is not None:
                # Check for sign change (crossing zero)
                if (previous_profit < 0 and profit > 0) or (previous_profit > 0 and profit < 0):
                    # Linear interpolation for approximate breakeven
                    if profit != previous_profit:
                        be = previous_price - previous_profit * (price - previous_price) / (profit - previous_profit)
                        if not breakevens or abs(be - breakevens[-1]) > 1:  # Avoid duplicates
                            breakevens.append(be)
            
            previous_profit = profit
            previous_price = price
        
        return sorted(set(round(be, 2) for be in breakevens))
    
    def profit_range(self, spot_price: float, num_points: int = 100) -> List[Tuple[float, float]]:
        """Generate profit/loss curve for graphing"""
        prices = self._get_test_prices(spot_price, granularity=100 / num_points)
        return [(price, self.profit_at_expiration(price)) for price in prices]
    
    def _get_test_prices(self, current_spot: float, granularity: float = 1.0) -> List[float]:
        """Generate test prices for analysis"""
        strikes = [leg.strike for leg in self.legs]
        min_strike = min(strikes)
        max_strike = max(strikes)
        
        # Range from 50% to 150% of strike range
        price_range = max_strike - min_strike
        start = min_strike - price_range * 0.5
        end = max_strike + price_range * 0.5
        
        num_steps = int((end - start) / granularity) + 1
        return [start + i * granularity for i in range(num_steps)]
    
    def summary(self, spot_price: float) -> Dict:
        """Generate strategy summary"""
        return {
            'name': self.name,
            'total_cost': self.total_cost(),
            'max_profit': self.max_profit(spot_price),
            'max_loss': self.max_loss(spot_price),
            'breakeven_points': self.breakeven_points(spot_price),
            'current_spot': spot_price,
            'legs': [
                {
                    'type': leg.option_type,
                    'strike': leg.strike,
                    'price': leg.price,
                    'position': 'long' if leg.premium_paid else 'short'
                }
                for leg in self.legs
            ]
        }


class StrategyBuilder:
    """Helper class to build common strategies"""
    
    @staticmethod
    def long_call(call_price: float, strike: float) -> OptionStrategy:
        """Simple long call"""
        return OptionStrategy(
            "Long Call",
            [Leg('call', strike, call_price, 1, True)]
        )
    
    @staticmethod
    def long_put(put_price: float, strike: float) -> OptionStrategy:
        """Simple long put"""
        return OptionStrategy(
            "Long Put",
            [Leg('put', strike, put_price, 1, True)]
        )
    
    @staticmethod
    def straddle(call_price: float, put_price: float, strike: float) -> OptionStrategy:
        """Long call + long put at same strike"""
        return OptionStrategy(
            "Long Straddle",
            [
                Leg('call', strike, call_price, 1, True),
                Leg('put', strike, put_price, 1, True)
            ]
        )
    
    @staticmethod
    def strangle(call_price: float, put_price: float, 
                 call_strike: float, put_strike: float) -> OptionStrategy:
        """Long call + long put at different strikes"""
        return OptionStrategy(
            "Long Strangle",
            [
                Leg('call', call_strike, call_price, 1, True),
                Leg('put', put_strike, put_price, 1, True)
            ]
        )
    
    @staticmethod
    def bull_call_spread(long_call_price: float, short_call_price: float,
                        long_strike: float, short_strike: float) -> OptionStrategy:
        """Long call + short call (higher strike)"""
        return OptionStrategy(
            "Bull Call Spread",
            [
                Leg('call', long_strike, long_call_price, 1, True),
                Leg('call', short_strike, short_call_price, 1, False)
            ]
        )
    
    @staticmethod
    def bear_put_spread(long_put_price: float, short_put_price: float,
                       long_strike: float, short_strike: float) -> OptionStrategy:
        """Long put + short put (lower strike)"""
        return OptionStrategy(
            "Bear Put Spread",
            [
                Leg('put', long_strike, long_put_price, 1, True),
                Leg('put', short_strike, short_put_price, 1, False)
            ]
        )
