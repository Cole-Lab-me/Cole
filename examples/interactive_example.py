"""
Interactive Option Pricing Simulator
Provides a menu-driven interface for option pricing and analysis
"""

import sys
from option_simulator import (
    BlackScholesCalculator,
    BinomialTreeCalculator,
    BinomialParams,
    MonteCarloSimulator,
    MonteCarloParams,
    StrategyBuilder
)


class OptionSimulatorCLI:
    """Interactive CLI for option pricing"""
    
    def __init__(self):
        self.spot = 100
        self.strike = 100
        self.time = 1
        self.rate = 0.05
        self.vol = 0.2
        self.div = 0.02
    
    def clear_screen(self):
        """Clear terminal screen"""
        print("\033[2J\033[H")
    
    def print_header(self, title):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"{title:^60}")
        print(f"{'='*60}\n")
    
    def print_current_params(self):
        """Print current parameters"""
        print("Current Parameters:")
        print(f"  Spot Price: ${self.spot}")
        print(f"  Strike Price: ${self.strike}")
        print(f"  Time to Expiry: {self.time} year(s)")
        print(f"  Risk-free Rate: {self.rate*100}%")
        print(f"  Volatility: {self.vol*100}%")
        print(f"  Dividend Yield: {self.div*100}%\n")
    
    def set_parameters(self):
        """Allow user to set parameters"""
        self.print_header("Set Parameters")
        
        try:
            self.spot = float(input(f"Spot Price [{self.spot}]: ") or self.spot)
            self.strike = float(input(f"Strike Price [{self.strike}]: ") or self.strike)
            self.time = float(input(f"Time to Expiry (years) [{self.time}]: ") or self.time)
            self.rate = float(input(f"Risk-free Rate [% {self.rate*100}]: ") or self.rate) / 100
            self.vol = float(input(f"Volatility [% {self.vol*100}]: ") or self.vol) / 100
            self.div = float(input(f"Dividend Yield [% {self.div*100}]: ") or self.div) / 100
            print("\n✓ Parameters updated successfully!")
        except ValueError:
            print("\n✗ Invalid input. Please enter numeric values.")
    
    def black_scholes_pricing(self):
        """Black-Scholes pricing menu"""
        self.print_header("Black-Scholes Pricing")
        self.print_current_params()
        
        try:
            calc = BlackScholesCalculator(
                spot_price=self.spot,
                strike_price=self.strike,
                time_to_expiry=self.time,
                risk_free_rate=self.rate,
                volatility=self.vol,
                dividend_yield=self.div
            )
            
            call_price = calc.call_price()
            put_price = calc.put_price()
            
            print(f"European Call Price: ${call_price:.4f}")
            print(f"European Put Price:  ${put_price:.4f}")
            
            print("\nCalculate Greeks? (y/n): ", end="")
            if input().lower() == 'y':
                call_greeks = calc.call_greeks()
                put_greeks = calc.put_greeks()
                
                print(f"\nCall Greeks:")
                print(f"  Delta: {call_greeks['delta']:.4f}")
                print(f"  Gamma: {call_greeks['gamma']:.6f}")
                print(f"  Vega:  {call_greeks['vega']:.4f}")
                print(f"  Theta: {call_greeks['theta']:.4f}")
                print(f"  Rho:   {call_greeks['rho']:.4f}")
                
                print(f"\nPut Greeks:")
                print(f"  Delta: {put_greeks['delta']:.4f}")
                print(f"  Gamma: {put_greeks['gamma']:.6f}")
                print(f"  Vega:  {put_greeks['vega']:.4f}")
                print(f"  Theta: {put_greeks['theta']:.4f}")
                print(f"  Rho:   {put_greeks['rho']:.4f}")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def binomial_pricing(self):
        """Binomial tree pricing menu"""
        self.print_header("Binomial Tree Pricing")
        self.print_current_params()
        
        try:
            steps = int(input("Number of steps [100]: ") or 100)
            
            params = BinomialParams(
                spot_price=self.spot,
                strike_price=self.strike,
                time_to_expiry=self.time,
                risk_free_rate=self.rate,
                volatility=self.vol,
                dividend_yield=self.div,
                steps=steps
            )
            
            binomial = BinomialTreeCalculator(params)
            
            eu_call = binomial.call_price(american=False)
            eu_put = binomial.put_price(american=False)
            us_call = binomial.call_price(american=True)
            us_put = binomial.put_price(american=True)
            
            print(f"\nEuropean Call: ${eu_call:.4f}")
            print(f"European Put:  ${eu_put:.4f}")
            print(f"American Call: ${us_call:.4f} (Premium: ${us_call - eu_call:.4f})")
            print(f"American Put:  ${us_put:.4f} (Premium: ${us_put - eu_put:.4f})")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def monte_carlo_pricing(self):
        """Monte Carlo pricing menu"""
        self.print_header("Monte Carlo Simulation")
        self.print_current_params()
        
        try:
            sims = int(input("Number of simulations [100000]: ") or 100000)
            steps = int(input("Number of steps [252]: ") or 252)
            
            params = MonteCarloParams(
                spot_price=self.spot,
                strike_price=self.strike,
                time_to_expiry=self.time,
                risk_free_rate=self.rate,
                volatility=self.vol,
                dividend_yield=self.div,
                num_simulations=sims,
                num_steps=steps
            )
            
            mc = MonteCarloSimulator(params)
            
            call_price, call_se = mc.vanilla_option_price('call')
            put_price, put_se = mc.vanilla_option_price('put')
            
            print(f"\nEuropean Call: ${call_price:.4f} ± ${call_se:.4f}")
            print(f"European Put:  ${put_price:.4f} ± ${put_se:.4f}")
            
            var_95 = mc.value_at_risk(0.95)
            var_99 = mc.value_at_risk(0.99)
            
            print(f"\nValue at Risk:")
            print(f"  95% VaR: {var_95*100:.2f}% (${self.spot * var_95:.2f})")
            print(f"  99% VaR: {var_99*100:.2f}% (${self.spot * var_99:.2f})")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def strategy_analysis(self):
        """Strategy analysis menu"""
        self.print_header("Strategy Analysis")
        
        strategies = {
            '1': ('Long Call', lambda: StrategyBuilder.long_call(5.0, self.strike)),
            '2': ('Long Put', lambda: StrategyBuilder.long_put(5.0, self.strike)),
            '3': ('Straddle', lambda: StrategyBuilder.straddle(5.0, 4.0, self.strike)),
            '4': ('Bull Call Spread', lambda: StrategyBuilder.bull_call_spread(5.0, 2.0, self.strike, self.strike + 10)),
            '5': ('Bear Put Spread', lambda: StrategyBuilder.bear_put_spread(3.0, 5.0, self.strike - 10, self.strike)),
        }
        
        print("Available Strategies:")
        for key, (name, _) in strategies.items():
            print(f"  {key}. {name}")
        print("  0. Back to main menu")
        
        choice = input("\nSelect strategy: ")
        
        if choice in strategies:
            name, builder = strategies[choice]
            strategy = builder()
            summary = strategy.summary(self.spot)
            
            self.print_header(f"Strategy: {name}")
            print(f"Total Cost: ${summary['total_cost']:.2f}")
            print(f"Max Profit: ${summary['max_profit']:.2f}")
            print(f"Max Loss: ${summary['max_loss']:.2f}")
            print(f"Breakeven Points: {[f'${be:.2f}' for be in summary['breakeven_points']]}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main menu loop"""
        while True:
            self.print_header("Option Pricing Simulator")
            self.print_current_params()
            
            print("Menu:")
            print("  1. Set Parameters")
            print("  2. Black-Scholes Pricing")
            print("  3. Binomial Tree Pricing")
            print("  4. Monte Carlo Simulation")
            print("  5. Strategy Analysis")
            print("  0. Exit")
            
            choice = input("\nSelect option: ")
            
            if choice == '1':
                self.set_parameters()
            elif choice == '2':
                self.black_scholes_pricing()
            elif choice == '3':
                self.binomial_pricing()
            elif choice == '4':
                self.monte_carlo_pricing()
            elif choice == '5':
                self.strategy_analysis()
            elif choice == '0':
                print("\nThank you for using Option Pricing Simulator!")
                sys.exit(0)
            else:
                print("\n✗ Invalid option. Please try again.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    cli = OptionSimulatorCLI()
    cli.run()
