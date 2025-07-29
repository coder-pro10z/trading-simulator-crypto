# Crypto Trading Simulator (Python) 🐍

A real-time cryptocurrency trading simulator that connects to CoinMarketCap's WebSocket feed to test trading strategies with live price data. Perfect for backtesting algorithms and learning trading concepts without financial risk.

## Token Compatibility

**Important**: This simulator only works with tokens/contracts that are available on CoinMarketCap's DEX platform.

### **How to Check Token Availability:**
1. Visit: `https://dex.coinmarketcap.com/token/solana/CONTRACT_ADDRESS/`
2. Replace `CONTRACT_ADDRESS` with your target token's contract address
3. If the page loads with trading data, the token is supported
4. If you get a 404 or no data, the token won't work with this simulator


## Features ✨

- **Real-time Data**: Live price feeds from CoinMarketCap WebSocket
- **Smart Trading Logic**: Automated buy/sell decisions based on price movements  
- **Risk Management**: Stop-loss and take-profit mechanisms
- **Comprehensive Analytics**: P&L tracking, win rates, and trade history
- **Auto-reconnection**: Handles network interruptions gracefully
- **Graceful Shutdown**: Proper portfolio valuation on exit

## Trading Strategy 📈

### **Buy Conditions:**
- **Initial Buy**: Invest $100 with first price received
- **3% Recovery Buy**: Re-enter when price recovers 3% from last sell
- **10% Fall Reinvest**: Dollar-cost average on significant dips

### **Sell Conditions:**
- **5% Stop Loss**: Automatically cut losses to preserve capital
- **10% Take Profit**: Lock in gains at target levels

### **Key Features:**
- Uses remaining balance after each trade (realistic compounding)
- Tracks unrealized P&L for open positions
- Calculates final portfolio value using last known price

## Quick Start 🚀

### Prerequisites
```bash
pip install websockets asyncio
```

### Installation & Usage
```bash
python trading_simulator.py
```

### Stop Simulation
```bash
Press Ctrl+C to stop early and see final results
```

## Sample Output 📊

```
🚀 Trading Simulator Started!
💰 Initial Investment: $100.00
⏱️  Runtime: 10 minutes
📋 Trading Rules:
   • Sell at 5% loss
   • Sell at 10% profit
   • Reinvest at 10% price fall
   • Buy back at 3% price recovery
--------------------------------------------------
🔌 Connected to CoinMarketCap WebSocket

🟢 INITIAL BUY
   Price: $0.00007383
   Coins: 1354428.67
   Investment: $100.00
------------------------------
🔴 LOSS - 5% Stop Loss
   Buy Price: $0.00007383
   Sell Price: $0.00007014
   P&L: $-5.00 (-5.00%)
   Balance: $95.00
------------------------------
🔄 BUY (3% Recovery Buy)
   Price: $0.00007224
   Coins: 1314935.06
   Investment: $95.00
------------------------------
🟢 PROFIT - 10% Take Profit
   Buy Price: $0.00007224
   Sell Price: $0.00007946
   P&L: $9.50 (+10.00%)
   Balance: $104.50
------------------------------

==================================================
📊 FINAL TRADING SUMMARY
==================================================
💰 Cash Balance: $0.00
🪙 Coin Holdings: 1200000.50 coins @ $0.00008124
📊 Position Value: $97.49
💹 Unrealized P&L: $2.49 (+2.62%)
🚀 Initial Investment: $100.00
💵 Final Portfolio Value: $97.49
📈 Total P&L: $-2.51 (-2.51%)
🔢 Total Trades: 8
✅ Profitable Trades: 3/8
🎯 Win Rate: 37.5%
⏱️  Runtime: 10.0 minutes
😔 OVERALL LOSS 📉
==================================================
```

## Configuration ⚙️

Modify trading parameters in the code:

```python
# In TradingSimulator.__init__()
self.initial_investment = 100.0      # Starting amount ($)
self.runtime_minutes = 10            # How long to run

# Trading thresholds
self.sell_loss_threshold = 0.05      # 5% stop loss
self.sell_profit_threshold = 0.10    # 10% take profit
self.reinvest_fall_threshold = 0.10  # 10% reinvest trigger
self.buy_up_threshold = 0.03         # 3% recovery buy

```


**Happy Trading! 📈 (Virtually, of course!)**
