import asyncio
import websockets
import json
import time
from datetime import datetime, timedelta

class TradingSimulator:
    def __init__(self, initial_investment=100.0):
        self.initial_investment = initial_investment
        self.current_balance = initial_investment
        self.coin_holdings = 0.0
        self.buy_price = None
        self.has_position = False
        self.total_trades = 0
        self.profitable_trades = 0
        self.start_time = datetime.now()
        self.runtime_minutes = 10
        self.last_price = None  # Track last known price
        
        # Trading rules
        self.sell_loss_threshold = 0.05  # 5% loss
        self.sell_profit_threshold = 0.10  # 10% profit
        self.reinvest_fall_threshold = 0.10  # 10% fall to reinvest
        self.buy_up_threshold = 0.03  # 3% up to buy back in
        
        # Track last sell price for buy-back logic
        self.last_sell_price = None
        
        print("🚀 Trading Simulator Started!")
        print(f"💰 Initial Investment: ${self.initial_investment:.2f}")
        print(f"⏱️  Runtime: {self.runtime_minutes} minutes")
        print("📋 Trading Rules:")
        print("   • Sell at 5% loss")
        print("   • Sell at 10% profit")
        print("   • Reinvest at 10% price fall")
        print("   • Buy back at 3% price recovery")
        print("-" * 50)
    
    def should_stop(self):
        """Check if simulation should stop after 10 minutes"""
        elapsed = datetime.now() - self.start_time
        return elapsed >= timedelta(minutes=self.runtime_minutes)
    
    def calculate_coins_for_investment(self, price, investment_amount):
        """Calculate how many coins we can buy with given amount"""
        return investment_amount / price
    
    def execute_buy(self, price, is_initial=False, reason=""):
        """Execute buy order with available balance"""
        if not self.has_position and self.current_balance > 0:
            investment_amount = self.current_balance
            self.coin_holdings = self.calculate_coins_for_investment(price, investment_amount)
            self.buy_price = price
            self.has_position = True
            
            if is_initial:
                buy_type = "🟢 INITIAL BUY"
            else:
                buy_type = f"🔄 BUY ({reason})" if reason else "🔄 BUY"
                
            print(f"{buy_type}")
            print(f"   Price: ${price:.8f}")
            print(f"   Coins: {self.coin_holdings:.2f}")
            print(f"   Investment: ${investment_amount:.2f}")
            
            self.current_balance = 0  # All available money invested
            print("-" * 30)
    
    def execute_sell(self, current_price, reason):
        """Execute sell order"""
        if self.has_position:
            # Track the sell price for potential buy-back
            self.last_sell_price = current_price
            
            # Calculate current value based on what we actually invested
            investment_amount = self.coin_holdings * self.buy_price
            current_value = self.coin_holdings * current_price
            profit_loss = current_value - investment_amount
            profit_loss_pct = (profit_loss / investment_amount) * 100
            
            # Update balances
            self.current_balance = current_value
            self.coin_holdings = 0
            self.has_position = False
            self.total_trades += 1
            
            if profit_loss > 0:
                self.profitable_trades += 1
                status = "🟢 PROFIT"
            else:
                status = "🔴 LOSS"
            
            print(f"{status} - {reason}")
            print(f"   Buy Price: ${self.buy_price:.8f}")
            print(f"   Sell Price: ${current_price:.8f}")
            print(f"   P&L: ${profit_loss:.2f} ({profit_loss_pct:+.2f}%)")
            print(f"   Balance: ${self.current_balance:.2f}")
            print("-" * 30)
            
            return profit_loss
        return 0
    
    def execute_reinvest(self, current_price):
        """Reinvest available balance (legacy method)"""
        if not self.has_position and self.current_balance > 0:
            self.execute_buy(current_price, is_initial=False, reason="Reinvest")
    
    def process_price_update(self, price):
        """Process new price and execute trading logic"""
        # Always update last known price
        self.last_price = price
        
        if self.should_stop():
            return False
        
        # Initial buy if we don't have position
        if not self.has_position and self.current_balance > 0:
            is_first_buy = self.total_trades == 0
            self.execute_buy(price, is_initial=is_first_buy)
            return True
        
        # If we have a position, check sell conditions
        if self.has_position:
            price_change_pct = (price - self.buy_price) / self.buy_price
            
            # Sell at 5% loss
            if price_change_pct <= -self.sell_loss_threshold:
                self.execute_sell(price, "5% Stop Loss")
                return True
            
            # Sell at 10% profit
            elif price_change_pct >= self.sell_profit_threshold:
                self.execute_sell(price, "10% Take Profit")
                return True
        
        # If no position but have balance, check buy conditions
        elif not self.has_position and self.current_balance > 0:
            should_buy = False
            buy_reason = ""
            
            # Check for 3% recovery buy (if we have a recent sell price)
            if self.last_sell_price and price >= self.last_sell_price * (1 + self.buy_up_threshold):
                should_buy = True
                buy_reason = "3% Recovery Buy"
            
            # Check for 10% fall reinvest (from previous buy price)
            elif self.buy_price and price <= self.buy_price * (1 - self.reinvest_fall_threshold):
                should_buy = True
                buy_reason = "10% Fall Reinvest"
            
            if should_buy:
                self.execute_buy(price, is_initial=False, reason=buy_reason)
                return True
        
        return True
    
    def display_final_summary(self):
        """Display final trading summary"""
        print("\n" + "=" * 50)
        print("📊 FINAL TRADING SUMMARY")
        print("=" * 50)
        
        # Calculate final balance (including any remaining position)
        final_balance = self.current_balance
        
        if self.has_position and self.last_price:
            # Calculate final position value using last known price
            position_value = self.coin_holdings * self.last_price
            final_balance = self.current_balance + position_value
            
            # Show what the final sell would be
            unrealized_pnl = position_value - (self.coin_holdings * self.buy_price)
            unrealized_pnl_pct = (unrealized_pnl / (self.coin_holdings * self.buy_price)) * 100
            
            print(f"💰 Cash Balance: ${self.current_balance:.2f}")
            print(f"🪙 Coin Holdings: {self.coin_holdings:.2f} coins @ ${self.last_price:.8f}")
            print(f"📊 Position Value: ${position_value:.2f}")
            print(f"💹 Unrealized P&L: ${unrealized_pnl:.2f} ({unrealized_pnl_pct:+.2f}%)")
            
        elif self.has_position:
            print(f"💰 Cash Balance: ${self.current_balance:.2f}")
            print(f"🪙 Coin Holdings: {self.coin_holdings:.2f} coins")
            print("   ⚠️  No final price available for position valuation")
        else:
            final_balance = self.current_balance
        
        total_pnl = final_balance - self.initial_investment
        total_pnl_pct = (total_pnl / self.initial_investment) * 100 if self.initial_investment > 0 else 0
        
        print(f"🚀 Initial Investment: ${self.initial_investment:.2f}")
        print(f"💵 Final Portfolio Value: ${final_balance:.2f}")
        print(f"📈 Total P&L: ${total_pnl:.2f} ({total_pnl_pct:+.2f}%)")
        print(f"🔢 Total Trades: {self.total_trades}")
        print(f"✅ Profitable Trades: {self.profitable_trades}/{self.total_trades}")
        
        if self.total_trades > 0:
            win_rate = (self.profitable_trades / self.total_trades) * 100
            print(f"🎯 Win Rate: {win_rate:.1f}%")
        
        runtime = datetime.now() - self.start_time
        print(f"⏱️  Runtime: {runtime.total_seconds()/60:.1f} minutes")
        
        # Show final status
        if total_pnl > 0:
            print("🎉 OVERALL PROFIT! 📈")
        elif total_pnl < 0:
            print("😔 OVERALL LOSS 📉")
        else:
            print("😐 BREAK EVEN")
        
        print("=" * 50)

class WebSocketTradingClient:
    def __init__(self, contract_address):
        self.contract_address = contract_address
        self.uri = "wss://dws.coinmarketcap.com/ws"
        self.subscription = {
            "method": "SUBSCRIPTION",
            "params": [f"quote@transaction@16_{self.contract_address}"]
        }
        self.simulator = TradingSimulator()
    
    async def connect_and_trade(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                print("🔌 Connected to CoinMarketCap WebSocket\n")
                
                # Send subscription
                await websocket.send(json.dumps(self.subscription))
                
                # Listen for messages
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        # print(f"📥 Received message: {data}")
                        
                        # Extract price from the message
                        if 'd' in data and 't0pu' in data['d']:
                            price = float(data['d']['t0pu'])
                            
                            # Process the price update
                            if not self.simulator.process_price_update(price):
                                break  # Time to stop
                        
                    except websockets.exceptions.ConnectionClosed:
                        print("Connection closed")
                        break
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.simulator.display_final_summary()

async def main():
    contract_address = input("Enter the contract address: ").strip()
    
    if not contract_address:
        print("⚠️ Contract address is required.")
        return
    
    client = WebSocketTradingClient(contract_address)
    await client.connect_and_trade()


if __name__ == "__main__":
    print("🎮 Crypto Trading Simulator")
    print("Press Ctrl+C to stop early\n")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user")
