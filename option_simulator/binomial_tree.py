"""
Binomial Tree Option Pricing Model
Implements the Cox-Ross-Rubinstein binomial tree for option pricing.
Supports both American and European options.
"""

import math
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class BinomialParams:
    """Parameters for binomial tree pricing"""
    spot_price: float
    strike_price: float
    time_to_expiry: float  # in years
    risk_free_rate: float
    volatility: float
    dividend_yield: float = 0.0
    steps: int = 100


class BinomialTreeCalculator:
    """Binomial tree option pricing calculator"""
    
    def __init__(self, params: BinomialParams):
        self.params = params
        self._validate_params()
        self._calculate_tree_params()
    
    def _validate_params(self):
        """Validate input parameters"""
        if self.params.spot_price <= 0:
            raise ValueError("Spot price must be positive")
        if self.params.strike_price <= 0:
            raise ValueError("Strike price must be positive")
        if self.params.time_to_expiry <= 0:
            raise ValueError("Time to expiry must be positive")
        if self.params.volatility <= 0:
            raise ValueError("Volatility must be positive")
        if self.params.steps < 1:
            raise ValueError("Steps must be at least 1")
    
    def _calculate_tree_params(self):
        """Calculate binomial tree parameters"""
        p = self.params
        dt = p.time_to_expiry / p.steps
        
        # Up and down factors
        self.u = math.exp(p.volatility * math.sqrt(dt))
        self.d = 1 / self.u
        
        # Risk-neutral probability
        self.q = (
            math.exp((p.risk_free_rate - p.dividend_yield) * dt) - self.d
        ) / (self.u - self.d)
        
        # Discount factor
        self.discount = math.exp(-p.risk_free_rate * dt)
    
    def _build_price_tree(self) -> list:
        """Build the underlying price tree"""
        p = self.params
        tree = [[0.0 for _ in range(i + 1)] for i in range(p.steps + 1)]
        
        # Initial price
        tree[0][0] = p.spot_price
        
        # Fill tree forward
        for i in range(1, p.steps + 1):
            for j in range(i + 1):
                tree[i][j] = p.spot_price * (self.u ** (i - j)) * (self.d ** j)
        
        return tree
    
    def _intrinsic_value(self, spot: float, option_type: str) -> float:
        """Calculate intrinsic value"""
        if option_type == 'call':
            return max(spot - self.params.strike_price, 0)
        else:  # put
            return max(self.params.strike_price - spot, 0)
    
    def european_option_price(self, option_type: str) -> float:
        """Calculate European option price"""
        price_tree = self._build_price_tree()
        p = self.params
        
        # Initialize option values at expiration
        option_values = [
            self._intrinsic_value(price_tree[p.steps][j], option_type)
            for j in range(p.steps + 1)
        ]
        
        # Work backwards through tree
        for i in range(p.steps - 1, -1, -1):
            option_values = [
                self.discount * (self.q * option_values[j] + (1 - self.q) * option_values[j + 1])
                for j in range(i + 1)
            ]
        
        return option_values[0]
    
    def american_option_price(self, option_type: str) -> float:
        """Calculate American option price (allows early exercise)"""
        price_tree = self._build_price_tree()
        p = self.params
        
        # Initialize option values at expiration
        option_values = [
            self._intrinsic_value(price_tree[p.steps][j], option_type)
            for j in range(p.steps + 1)
        ]
        
        # Work backwards through tree
        for i in range(p.steps - 1, -1, -1):
            for j in range(i + 1):
                # Continuation value
                continuation = self.discount * (
                    self.q * option_values[j] + (1 - self.q) * option_values[j + 1]
                )
                
                # Exercise value
                exercise = self._intrinsic_value(price_tree[i][j], option_type)
                
                # Take maximum (early exercise if beneficial)
                option_values[j] = max(exercise, continuation)
        
        return option_values[0]
    
    def call_price(self, american: bool = False) -> float:
        """Calculate call option price"""
        if american:
            return self.american_option_price('call')
        else:
            return self.european_option_price('call')
    
    def put_price(self, american: bool = False) -> float:
        """Calculate put option price"""
        if american:
            return self.american_option_price('put')
        else:
            return self.european_option_price('put')
