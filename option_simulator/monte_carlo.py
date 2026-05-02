"""
Monte Carlo Option Pricing Simulator
Implements Monte Carlo simulation for vanilla and exotic options
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class MonteCarloParams:
    """Parameters for Monte Carlo simulation"""
    spot_price: float
    strike_price: float
    time_to_expiry: float  # in years
    risk_free_rate: float
    volatility: float
    dividend_yield: float = 0.0
    num_simulations: int = 100000
    num_steps: int = 252


class MonteCarloSimulator:
    """Monte Carlo option pricing simulator"""
    
    def __init__(self, params: MonteCarloParams):
        self.params = params
        self._validate_params()
        self.dt = params.time_to_expiry / params.num_steps
        self.discount_factor = math.exp(-params.risk_free_rate * params.time_to_expiry)
    
    def _validate_params(self):
        """Validate parameters"""
        if self.params.spot_price <= 0:
            raise ValueError("Spot price must be positive")
        if self.params.strike_price <= 0:
            raise ValueError("Strike price must be positive")
        if self.params.time_to_expiry <= 0:
            raise ValueError("Time to expiry must be positive")
        if self.params.volatility <= 0:
            raise ValueError("Volatility must be positive")
        if self.params.num_simulations < 1:
            raise ValueError("Number of simulations must be positive")
    
    def _generate_paths(self) -> np.ndarray:
        """Generate stock price paths using geometric Brownian motion"""
        p = self.params
        
        # Initialize paths array
        paths = np.zeros((p.num_simulations, p.num_steps + 1))
        paths[:, 0] = p.spot_price
        
        # Generate random normal increments
        z = np.random.standard_normal((p.num_simulations, p.num_steps))
        
        # Generate paths
        for t in range(1, p.num_steps + 1):
            drift = (p.risk_free_rate - p.dividend_yield - 0.5 * p.volatility ** 2) * self.dt
            diffusion = p.volatility * math.sqrt(self.dt) * z[:, t - 1]
            paths[:, t] = paths[:, t - 1] * np.exp(drift + diffusion)
        
        return paths
    
    def vanilla_option_price(self, option_type: str) -> Tuple[float, float]:
        """Calculate vanilla option price and standard error"""
        paths = self._generate_paths()
        final_prices = paths[:, -1]
        
        if option_type == 'call':
            payoffs = np.maximum(final_prices - self.params.strike_price, 0)
        else:  # put
            payoffs = np.maximum(self.params.strike_price - final_prices, 0)
        
        option_prices = payoffs * self.discount_factor
        price = np.mean(option_prices)
        se = np.std(option_prices) / math.sqrt(self.params.num_simulations)
        
        return price, se
    
    def asian_option_price(self, option_type: str) -> Tuple[float, float]:
        """Calculate Asian option price (arithmetic average)"""
        paths = self._generate_paths()
        average_prices = np.mean(paths, axis=1)
        
        if option_type == 'call':
            payoffs = np.maximum(average_prices - self.params.strike_price, 0)
        else:  # put
            payoffs = np.maximum(self.params.strike_price - average_prices, 0)
        
        option_prices = payoffs * self.discount_factor
        price = np.mean(option_prices)
        se = np.std(option_prices) / math.sqrt(self.params.num_simulations)
        
        return price, se
    
    def barrier_option_price(self, option_type: str, barrier_level: float, 
                            knock_type: str = 'out') -> Tuple[float, float]:
        """Calculate barrier option price (knock-in or knock-out)"""
        paths = self._generate_paths()
        
        # Check if barrier was hit for each path
        if knock_type == 'out':
            # Option becomes worthless if barrier is hit
            hit_barrier = np.any(paths >= barrier_level, axis=1)
            active_paths = ~hit_barrier
        else:  # knock_type == 'in'
            # Option only activates if barrier is hit
            hit_barrier = np.any(paths >= barrier_level, axis=1)
            active_paths = hit_barrier
        
        final_prices = paths[:, -1]
        
        if option_type == 'call':
            payoffs = np.maximum(final_prices - self.params.strike_price, 0)
        else:  # put
            payoffs = np.maximum(self.params.strike_price - final_prices, 0)
        
        # Zero out payoffs for inactive paths
        payoffs[~active_paths] = 0
        
        option_prices = payoffs * self.discount_factor
        price = np.mean(option_prices)
        se = np.std(option_prices) / math.sqrt(self.params.num_simulations)
        
        return price, se
    
    def lookback_option_price(self, option_type: str) -> Tuple[float, float]:
        """Calculate lookback option price"""
        paths = self._generate_paths()
        
        if option_type == 'call':
            # Lookback call: max(max(S) - K, 0)
            max_prices = np.max(paths, axis=1)
            payoffs = np.maximum(max_prices - self.params.strike_price, 0)
        else:  # put
            # Lookback put: max(K - min(S), 0)
            min_prices = np.min(paths, axis=1)
            payoffs = np.maximum(self.params.strike_price - min_prices, 0)
        
        option_prices = payoffs * self.discount_factor
        price = np.mean(option_prices)
        se = np.std(option_prices) / math.sqrt(self.params.num_simulations)
        
        return price, se
    
    def value_at_risk(self, confidence_level: float) -> float:
        """Calculate Value at Risk (VaR)"""
        paths = self._generate_paths()
        final_prices = paths[:, -1]
        
        # Calculate returns
        returns = (final_prices - self.params.spot_price) / self.params.spot_price
        
        # VaR at confidence level
        var = np.percentile(returns, (1 - confidence_level) * 100)
        
        return abs(var)
    
    def conditional_value_at_risk(self, confidence_level: float) -> float:
        """Calculate Conditional Value at Risk (CVaR) / Expected Shortfall"""
        paths = self._generate_paths()
        final_prices = paths[:, -1]
        
        # Calculate returns
        returns = (final_prices - self.params.spot_price) / self.params.spot_price
        
        # CVaR: average of losses beyond VaR
        var_level = np.percentile(returns, (1 - confidence_level) * 100)
        cvar = np.mean(returns[returns <= var_level])
        
        return abs(cvar)
    
    def price_distribution(self) -> dict:
        """Get statistics of final price distribution"""
        paths = self._generate_paths()
        final_prices = paths[:, -1]
        
        return {
            'mean': np.mean(final_prices),
            'std': np.std(final_prices),
            'min': np.min(final_prices),
            'max': np.max(final_prices),
            'percentile_5': np.percentile(final_prices, 5),
            'percentile_25': np.percentile(final_prices, 25),
            'percentile_50': np.percentile(final_prices, 50),
            'percentile_75': np.percentile(final_prices, 75),
            'percentile_95': np.percentile(final_prices, 95)
        }
