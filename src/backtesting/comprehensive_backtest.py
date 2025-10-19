"""
Comprehensive Backtesting for All 7 Trading Pairs
Smart Money Trading System - Full Performance Analysis
"""

import sys
sys.path.append('web_app')

from trading_system import DayTradingSmartMoney, InstitutionalPatternDetector
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

def comprehensive_backtest():
    """Run backtesting on all 7 pairs"""
    
    # All 7 trading pairs with their Yahoo Finance symbols
    all_pairs = {
        'NAS100': 'NDX',       # NASDAQ 100 Index
        'US30': 'DJI',         # Dow Jones Index
        'GBPJPY': 'GBPJPY=X',  # GBP/JPY
        'CADCHF': 'CADCHF=X',  # CAD/CHF
        'USDJPY': 'USDJPY=X',  # USD/JPY
        'EURCAD': 'EURCAD=X',  # EUR/CAD
        'USDCAD': 'USDCAD=X'   # USD/CAD
    }
    
    print("🚀 COMPREHENSIVE SMART MONEY BACKTESTING")
    print("=" * 60)
    print(f"📊 Testing {len(all_pairs)} pairs with institutional patterns")
    print(f"📅 Period: 6 months of data")
    print(f"⚙️ Strategy: Smart Money + Day Trading")
    print("=" * 60)
    
    results = {}
    
    for pair_name, symbol in all_pairs.items():
        print(f"\n🔍 BACKTESTING: {pair_name} ({symbol})")
        print("-" * 40)
        
        try:
            # Download 6 months of historical data  
            end_date = datetime(2024, 12, 1)  # December 2024
            start_date = datetime(2024, 6, 1)  # June 2024 (6 months historical)
            
            print(f"📥 Downloading data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            data = yf.download(symbol, start=start_date, end=end_date, interval='1h')
            
            if data.empty:
                print(f"❌ No data available for {pair_name}")
                continue
                
            print(f"✅ Downloaded {len(data)} hours of data")
            
            # Initialize trading system
            trader = DayTradingSmartMoney(initial_capital=10000)
            detector = InstitutionalPatternDetector()
            
            # Run backtesting
            total_trades = 0
            winning_trades = 0
            losing_trades = 0
            total_profit = 0
            max_drawdown = 0
            peak_capital = 10000
            
            for i in range(50, len(data)):  # Start after enough data for indicators
                current_data = data.iloc[:i+1]
                
                # Detect smart money patterns
                signal = detector.detect_smart_money_entry(current_data)
                
                if signal:
                    current_price = data.iloc[i]['Close']
                    
                    # Calculate position size (2% risk)
                    risk_amount = trader.capital * 0.02
                    
                    if signal['direction'] == 'BUY':
                        stop_loss = current_price * 0.99  # 1% stop loss
                        take_profit = current_price * 1.02  # 2% take profit
                    else:
                        stop_loss = current_price * 1.01  # 1% stop loss
                        take_profit = current_price * 0.98  # 2% take profit
                    
                    # Simulate trade outcome (simplified)
                    # Look ahead 24 hours to see if TP or SL hit
                    future_end = min(i + 24, len(data) - 1)
                    future_data = data.iloc[i+1:future_end+1]
                    
                    trade_outcome = simulate_trade_outcome(
                        current_price, signal['direction'], 
                        stop_loss, take_profit, future_data
                    )
                    
                    total_trades += 1
                    
                    if trade_outcome > 0:
                        winning_trades += 1
                        total_profit += trade_outcome
                    else:
                        losing_trades += 1
                        total_profit += trade_outcome
                    
                    # Update capital
                    trader.capital += trade_outcome
                    
                    # Track drawdown
                    if trader.capital > peak_capital:
                        peak_capital = trader.capital
                    
                    current_drawdown = (peak_capital - trader.capital) / peak_capital * 100
                    max_drawdown = max(max_drawdown, current_drawdown)
            
            # Calculate metrics
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            total_return = (trader.capital - 10000) / 10000 * 100
            
            results[pair_name] = {
                'symbol': symbol,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': win_rate,
                'total_return': total_return,
                'final_capital': trader.capital,
                'max_drawdown': max_drawdown,
                'profit_loss': total_profit
            }
            
            print(f"📈 RESULTS for {pair_name}:")
            print(f"   💰 Total Return: {total_return:.2f}%")
            print(f"   🎯 Win Rate: {win_rate:.1f}%")
            print(f"   📊 Total Trades: {total_trades}")
            print(f"   💵 Final Capital: ${trader.capital:.2f}")
            print(f"   📉 Max Drawdown: {max_drawdown:.2f}%")
            
        except Exception as e:
            print(f"❌ Error backtesting {pair_name}: {e}")
            continue
    
    # Print comprehensive summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE RESULTS SUMMARY")
    print("=" * 60)
    
    if results:
        # Sort by total return
        sorted_results = sorted(results.items(), key=lambda x: x[1]['total_return'], reverse=True)
        
        print(f"{'Pair':<8} {'Return%':<8} {'WinRate%':<9} {'Trades':<7} {'Risk':<6}")
        print("-" * 50)
        
        total_return_all = 0
        total_trades_all = 0
        
        for pair_name, metrics in sorted_results:
            return_pct = metrics['total_return']
            win_rate = metrics['win_rate']
            trades = metrics['total_trades']
            
            # Risk assessment
            if win_rate >= 60 and return_pct >= 0:
                risk = "🟢 LOW"
            elif win_rate >= 50 or return_pct >= 0:
                risk = "🟡 MED"
            else:
                risk = "🔴 HIGH"
            
            print(f"{pair_name:<8} {return_pct:>6.1f}% {win_rate:>7.1f}% {trades:>6} {risk}")
            
            total_return_all += return_pct
            total_trades_all += trades
        
        avg_return = total_return_all / len(results)
        
        print("-" * 50)
        print(f"{'AVERAGE':<8} {avg_return:>6.1f}% {'':>7} {total_trades_all:>6}")
        
        print(f"\n🏆 BEST PERFORMER: {sorted_results[0][0]} ({sorted_results[0][1]['total_return']:.1f}%)")
        print(f"🎯 HIGHEST WIN RATE: {max(results.items(), key=lambda x: x[1]['win_rate'])[0]} ({max(results.items(), key=lambda x: x[1]['win_rate'])[1]['win_rate']:.1f}%)")
        
        # Risk distribution
        low_risk = sum(1 for _, m in results.items() if m['win_rate'] >= 60 and m['total_return'] >= 0)
        med_risk = sum(1 for _, m in results.items() if (m['win_rate'] >= 50 or m['total_return'] >= 0) and not (m['win_rate'] >= 60 and m['total_return'] >= 0))
        high_risk = len(results) - low_risk - med_risk
        
        print(f"\n📊 RISK DISTRIBUTION:")
        print(f"   🟢 Low Risk: {low_risk} pairs")
        print(f"   🟡 Medium Risk: {med_risk} pairs") 
        print(f"   🔴 High Risk: {high_risk} pairs")
        
    else:
        print("❌ No successful backtests completed")
    
    return results

def simulate_trade_outcome(entry_price, direction, stop_loss, take_profit, future_data):
    """Simulate trade outcome based on future price action"""
    
    if future_data.empty:
        return -100  # Small loss if no data
    
    for _, candle in future_data.iterrows():
        high = candle['High']
        low = candle['Low']
        
        if direction == 'BUY':
            # Check if stop loss hit
            if low <= stop_loss:
                return -200  # Stop loss hit
            # Check if take profit hit  
            elif high >= take_profit:
                return 400  # Take profit hit
        else:  # SELL
            # Check if stop loss hit
            if high >= stop_loss:
                return -200  # Stop loss hit
            # Check if take profit hit
            elif low <= take_profit:
                return 400  # Take profit hit
    
    # If neither TP nor SL hit, simulate market close (small profit/loss)
    close_price = future_data.iloc[-1]['Close']
    
    if direction == 'BUY':
        return (close_price - entry_price) / entry_price * 2000 if close_price > entry_price else -100
    else:
        return (entry_price - close_price) / entry_price * 2000 if close_price < entry_price else -100

if __name__ == "__main__":
    results = comprehensive_backtest()