"""
Black-Scholes Option Pricing Model
Implements the Black-Scholes formula for European option pricing with Greeks
"""

import math
from dataclasses import dataclass
from scipy.stats import norm
from scipy.optimize import brentq


@dataclass
class BlackScholesCalculator:
    """Black-Scholes European option pricing calculator"""
    
    spot_price: float
    strike_price: float
    time_to_expiry: float  # in years
    risk_free_rate: float
    volatility: float  # annualized
    dividend_yield: float = 0.0
    
    def __post_init__(self):
        """Validate parameters after initialization"""
        self._validate_params()
    
    def _validate_params(self):
        """Validate input parameters"""
        if self.spot_price <= 0:
            raise ValueError("Spot price must be positive")
        if self.strike_price <= 0:
            raise ValueError("Strike price must be positive")
        if self.time_to_expiry <= 0:
            raise ValueError("Time to expiry must be positive")
        if self.volatility <= 0:
            raise ValueError("Volatility must be positive")
    
    def _d1(self) -> float:
        """Calculate d1 parameter"""
        numerator = math.log(self.spot_price / self.strike_price) + (
            self.risk_free_rate - self.dividend_yield + 0.5 * self.volatility ** 2
        ) * self.time_to_expiry
        denominator = self.volatility * math.sqrt(self.time_to_expiry)
        return numerator / denominator
    
    def _d2(self) -> float:
        """Calculate d2 parameter"""
        return self._d1() - self.volatility * math.sqrt(self.time_to_expiry)
    
    def call_price(self) -> float:
        """Calculate European call option price"""
        d1 = self._d1()
        d2 = self._d2()
        
        call = (
            self.spot_price * math.exp(-self.dividend_yield * self.time_to_expiry) * norm.cdf(d1)
            - self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(d2)
        )
        
        return call
    
    def put_price(self) -> float:
        """Calculate European put option price"""
        d1 = self._d1()
        d2 = self._d2()
        
        put = (
            self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(-d2)
            - self.spot_price * math.exp(-self.dividend_yield * self.time_to_expiry) * norm.cdf(-d1)
        )
        
        return put
    
    def call_greeks(self) -> dict:
        """Calculate call option Greeks"""
        d1 = self._d1()
        d2 = self._d2()
        
        delta = math.exp(-self.dividend_yield * self.time_to_expiry) * norm.cdf(d1)
        gamma = (
            math.exp(-self.dividend_yield * self.time_to_expiry) * norm.pdf(d1)
            / (self.spot_price * self.volatility * math.sqrt(self.time_to_expiry))
        )
        vega = (
            self.spot_price * math.exp(-self.dividend_yield * self.time_to_expiry)
            * norm.pdf(d1) * math.sqrt(self.time_to_expiry) / 100
        )
        theta = (
            -(self.spot_price * math.exp(-self.dividend_yield * self.time_to_expiry)
              * norm.pdf(d1) * self.volatility) / (2 * math.sqrt(self.time_to_expiry))
            - self.risk_free_rate * self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(d2)
        ) / 365
        rho = (
            self.strike_price * self.time_to_expiry
            * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(d2) / 100
        )
        
        return {
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho
        }
    
    def put_greeks(self) -> dict:
        """Calculate put option Greeks"""
        d1 = self._d1()
        d2 = self._d2()
        
        delta = math.exp(-self.dividend_yield * self.time_to_expiry) * (norm.cdf(d1) - 1)
        gamma = (
            math.exp(-self.dividend_yield * self.time_to_expiry) * norm.pdf(d1)
            / (self.spot_price * self.volatility * math.sqrt(self.time_to_expiry))
        )
        vega = (
            self.spot_price * math.exp(-self.dividend_yield * self.time_to_expiry)
            * norm.pdf(d1) * math.sqrt(self.time_to_expiry) / 100
        )
        theta = (
            -(self.spot_price * math.exp(-self.dividend_yield * self.time_to_expiry)
              * norm.pdf(d1) * self.volatility) / (2 * math.sqrt(self.time_to_expiry))
            + self.risk_free_rate * self.strike_price * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(-d2)
        ) / 365
        rho = (
            -self.strike_price * self.time_to_expiry
            * math.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(-d2) / 100
        )
        
        return {
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho
        }
    
    def implied_volatility(self, market_price: float, option_type: str = 'call', tol: float = 1e-6) -> float:
        """Calculate implied volatility using Newton-Raphson method"""
        
        def objective(vol):
            temp_calc = BlackScholesCalculator(
                spot_price=self.spot_price,
                strike_price=self.strike_price,
                time_to_expiry=self.time_to_expiry,
                risk_free_rate=self.risk_free_rate,
                volatility=vol,
                dividend_yield=self.dividend_yield
            )
            
            if option_type == 'call':
                return temp_calc.call_price() - market_price
            else:
                return temp_calc.put_price() - market_price
        
        # Use Brent's method for root finding
        try:
            iv = brentq(objective, 0.001, 5.0, xtol=tol)
            return iv
        except ValueError:
            return None
