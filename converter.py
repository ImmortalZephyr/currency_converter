"""
💱 Currency Converter Pro
Real-time currency conversion with live exchange rates
Supports 150+ currencies with beautiful CLI interface
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class CurrencyConverter:
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.cache_file = "currency_cache.json"
        self.rates: Dict[str, float] = {}
        self.last_update: Optional[str] = None
        self.popular_currencies = {
            'USD': '🇺🇸 US Dollar',
            'EUR': '🇪🇺 Euro',
            'GBP': '🇬🇧 British Pound',
            'JPY': '🇯🇵 Japanese Yen',
            'AUD': '🇦🇺 Australian Dollar',
            'CAD': '🇨🇦 Canadian Dollar',
            'CHF': '🇨🇭 Swiss Franc',
            'CNY': '🇨🇳 Chinese Yuan',
            'INR': '🇮🇳 Indian Rupee',
            'VND': '🇻🇳 Vietnamese Dong',
            'KRW': '🇰🇷 South Korean Won',
            'SGD': '🇸🇬 Singapore Dollar',
            'THB': '🇹🇭 Thai Baht',
            'MYR': '🇲🇾 Malaysian Ringgit',
            'PHP': '🇵🇭 Philippine Peso',
            'BTC': '₿ Bitcoin',
        }
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        header = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║            💱 CURRENCY CONVERTER PRO 💱                  ║
║          Real-time Exchange Rates & Conversion           ║
╚══════════════════════════════════════════════════════════╝
{Colors.END}"""
        print(header)
        if self.last_update:
            print(f"{Colors.YELLOW}Last Update: {self.last_update}{Colors.END}\n")
    
    def fetch_rates(self, base_currency: str = 'USD') -> bool:
        """Fetch exchange rates from API"""
        try:
            print(f"{Colors.YELLOW}📡 Fetching latest rates...{Colors.END}")
            response = requests.get(f"{self.base_url}{base_currency}", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.rates = data['rates']
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save to cache
            self.save_cache()
            
            print(f"{Colors.GREEN}✓ Rates updated successfully!{Colors.END}\n")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}✗ Failed to fetch rates: {e}{Colors.END}")
            print(f"{Colors.YELLOW}Trying to load from cache...{Colors.END}\n")
            return self.load_cache()
    
    def save_cache(self):
        """Save rates to cache file"""
        cache_data = {
            'rates': self.rates,
            'last_update': self.last_update
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)
    
    def load_cache(self) -> bool:
        """Load rates from cache file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    self.rates = cache_data['rates']
                    self.last_update = cache_data['last_update']
                print(f"{Colors.GREEN}✓ Loaded from cache{Colors.END}\n")
                return True
        except Exception as e:
            print(f"{Colors.RED}✗ Cache load failed: {e}{Colors.END}\n")
        return False
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[float]:
        """Convert amount from one currency to another"""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency not in self.rates or to_currency not in self.rates:
            return None
        
        # Convert to USD first, then to target currency
        amount_in_usd = amount / self.rates[from_currency]
        result = amount_in_usd * self.rates[to_currency]
        
        return result
    
    def show_popular_currencies(self):
        """Display popular currencies"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}🌟 POPULAR CURRENCIES{Colors.END}")
        print(f"{Colors.CYAN}{'='*58}{Colors.END}")
        
        for code, name in self.popular_currencies.items():
            if code in self.rates:
                rate = self.rates[code]
                print(f"{Colors.YELLOW}{code:4}{Colors.END} - {name:30} Rate: {Colors.GREEN}{rate:.4f}{Colors.END}")
        print()
    
    def search_currency(self, keyword: str) -> List[str]:
        """Search for currencies by keyword"""
        keyword = keyword.upper()
        results = [code for code in self.rates.keys() if keyword in code]
        return results[:10]  # Limit to 10 results
    
    def show_conversion_table(self, base_currency: str, amount: float):
        """Show conversion table for popular currencies"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}📊 CONVERSION TABLE{Colors.END}")
        print(f"{Colors.CYAN}Base: {amount} {base_currency.upper()}{Colors.END}")
        print(f"{Colors.CYAN}{'='*58}{Colors.END}")
        
        for code in ['USD', 'EUR', 'GBP', 'JPY', 'VND', 'CNY']:
            if code != base_currency.upper() and code in self.rates:
                converted = self.convert(amount, base_currency, code)
                if converted:
                    flag = self.popular_currencies.get(code, '').split()[0]
                    print(f"{flag} {code:4}: {Colors.GREEN}{converted:,.2f}{Colors.END}")
        print()
    
    def interactive_mode(self):
        """Run interactive conversion mode"""
        while True:
            try:
                print(f"{Colors.BOLD}Enter conversion details:{Colors.END}")
                amount = input(f"{Colors.BLUE}Amount: {Colors.END}").strip()
                
                if amount.lower() in ['quit', 'exit', 'q']:
                    break
                
                try:
                    amount = float(amount)
                except ValueError:
                    print(f"{Colors.RED}✗ Invalid amount!{Colors.END}\n")
                    continue
                
                from_curr = input(f"{Colors.BLUE}From (e.g., USD): {Colors.END}").strip().upper()
                to_curr = input(f"{Colors.BLUE}To (e.g., VND): {Colors.END}").strip().upper()
                
                if from_curr not in self.rates:
                    print(f"{Colors.RED}✗ Currency '{from_curr}' not found!{Colors.END}\n")
                    continue
                
                if to_curr not in self.rates:
                    print(f"{Colors.RED}✗ Currency '{to_curr}' not found!{Colors.END}\n")
                    continue
                
                result = self.convert(amount, from_curr, to_curr)
                
                if result:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}💰 RESULT:{Colors.END}")
                    print(f"{Colors.CYAN}{amount:,.2f} {from_curr}{Colors.END} = {Colors.GREEN}{Colors.BOLD}{result:,.2f} {to_curr}{Colors.END}")
                    
                    # Show exchange rate
                    rate = self.rates[to_curr] / self.rates[from_curr]
                    print(f"{Colors.YELLOW}Exchange Rate: 1 {from_curr} = {rate:.6f} {to_curr}{Colors.END}\n")
                    
                    # Ask if want to see conversion table
                    show_table = input(f"{Colors.BLUE}Show conversion table? (y/n): {Colors.END}").strip().lower()
                    if show_table == 'y':
                        self.show_conversion_table(from_curr, amount)
                else:
                    print(f"{Colors.RED}✗ Conversion failed!{Colors.END}\n")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Exiting...{Colors.END}\n")
                break
            except Exception as e:
                print(f"{Colors.RED}✗ Error: {e}{Colors.END}\n")
    
    def show_menu(self):
        """Display main menu"""
        menu = f"""
{Colors.CYAN}{Colors.BOLD}MENU OPTIONS:{Colors.END}
{Colors.YELLOW}1.{Colors.END} Convert Currency
{Colors.YELLOW}2.{Colors.END} Show Popular Currencies
{Colors.YELLOW}3.{Colors.END} Search Currency
{Colors.YELLOW}4.{Colors.END} Refresh Rates
{Colors.YELLOW}5.{Colors.END} Exit

{Colors.BLUE}Choice: {Colors.END}"""
        return input(menu).strip()
    
    def run(self):
        """Main application loop"""
        self.clear_screen()
        self.print_header()
        
        # Initial fetch
        if not self.fetch_rates():
            print(f"{Colors.RED}Failed to load rates. Please check your internet connection.{Colors.END}")
            return
        
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                print()
                self.interactive_mode()
            
            elif choice == '2':
                self.show_popular_currencies()
            
            elif choice == '3':
                keyword = input(f"\n{Colors.BLUE}Search currency (e.g., VN): {Colors.END}").strip()
                results = self.search_currency(keyword)
                if results:
                    print(f"\n{Colors.GREEN}Found currencies:{Colors.END}")
                    for code in results:
                        print(f"{Colors.YELLOW}- {code}{Colors.END}")
                    print()
                else:
                    print(f"{Colors.RED}No currencies found!{Colors.END}\n")
            
            elif choice == '4':
                print()
                self.fetch_rates()
            
            elif choice == '5':
                print(f"\n{Colors.GREEN}Thank you for using Currency Converter Pro! 💱{Colors.END}\n")
                break
            
            else:
                print(f"{Colors.RED}Invalid choice!{Colors.END}\n")

def main():
    """Entry point"""
    converter = CurrencyConverter()
    converter.run()

if __name__ == "__main__":
    main()