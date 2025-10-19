#!/usr/bin/env python3
"""
Real Data Backtesting - Full System Test
Comprehensive backtesting using actual historical market data from yfinance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from index import get_real_market_data
from trading_system import InstitutionalPatternDetector, DayTradingSmartMoney
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def backtest_real_data(symbol, pair_name, days=30, initial_capital=10000):
    """Backtest trading system on real historical data"""
    
    print(f"\n🔥 BACKTESTING {pair_name} WITH REAL DATA")
    print("=" * 50)
    
    try:
        # Get real historical data from yfinance
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=f"{days}d", interval="1h")
        
        if len(data) < 50:
            print(f"❌ Insufficient data for {pair_name}")
            return None
        
        print(f"📊 Data Retrieved: {len(data)} hours of real market data")
        print(f"📅 Period: {data.index[0].strftime('%Y-%m-%d %H:%M')} to {data.index[-1].strftime('%Y-%m-%d %H:%M')}")
        print(f"💰 Price Range: {data['Low'].min():.4f} - {data['High'].max():.4f}")
        
        # Initialize trading systems
        pattern_detector = InstitutionalPatternDetector()
        trader = DayTradingSmartMoney(initial_capital=initial_capital)
        
        # Track results
        trades = []
        equity_curve = [initial_capital]
        
        # Analyze market data in chunks for realistic simulation
        chunk_size = 24  # 24-hour chunks
        total_chunks = len(data) // chunk_size
        
        print(f"\n🎯 RUNNING BACKTEST ({total_chunks} trading sessions)...")
        
        for i in range(1, total_chunks):
            # Get data chunk for analysis
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(data))
            chunk_data = data.iloc[start_idx:end_idx]
            
            if len(chunk_data) < 10:
                continue
            
            # Detect patterns in this chunk
            signals = pattern_detector.analyze_patterns(chunk_data)
            
            if signals:
                for signal in signals[:2]:  # Max 2 trades per session
                    # Execute trade with real market conditions
                    current_bar = chunk_data.iloc[-1]
                    trade_result = trader.execute_trade(signal, current_bar)
                    
                    if trade_result:
                        # Simulate trade outcome based on subsequent price action
                        if end_idx < len(data):
                            future_data = data.iloc[end_idx:end_idx+12]  # Next 12 hours
                            
                            if len(future_data) > 0:
                                exit_price = future_data['Close'].iloc[-1]
                                
                                # Calculate trade result
                                if signal['direction'] == 'BUY':
                                    pnl = (exit_price - trade_result['entry_price']) * trade_result['position_size']
                                else:
                                    pnl = (trade_result['entry_price'] - exit_price) * trade_result['position_size']
                                
                                # Apply realistic spread/commission
                                commission = abs(trade_result['position_size'] * trade_result['entry_price'] * 0.0001)
                                final_pnl = pnl - commission
                                
                                trade_record = {
                                    'timestamp': current_bar.name,
                                    'pair': pair_name,
                                    'direction': signal['direction'],
                                    'entry_price': trade_result['entry_price'],
                                    'exit_price': exit_price,
                                    'position_size': trade_result['position_size'],
                                    'pnl': final_pnl,
                                    'pattern': signal['pattern'],
                                    'confidence': signal['confidence']
                                }
                                
                                trades.append(trade_record)
                                equity_curve.append(equity_curve[-1] + final_pnl)
        
        # Calculate performance metrics
        if trades:
            total_trades = len(trades)
            winning_trades = len([t for t in trades if t['pnl'] > 0])
            losing_trades = total_trades - winning_trades
            
            total_pnl = sum(t['pnl'] for t in trades)
            win_rate = (winning_trades / total_trades) * 100
            
            avg_win = np.mean([t['pnl'] for t in trades if t['pnl'] > 0]) if winning_trades > 0 else 0
            avg_loss = np.mean([t['pnl'] for t in trades if t['pnl'] < 0]) if losing_trades > 0 else 0
            
            profit_factor = abs(avg_win * winning_trades / (avg_loss * losing_trades)) if losing_trades > 0 else float('inf')
            
            final_balance = initial_capital + total_pnl
            total_return = (total_pnl / initial_capital) * 100
            
            # Display results
            print(f"\n📈 BACKTEST RESULTS FOR {pair_name}:")
            print("-" * 40)
            print(f"💰 Initial Capital: ${initial_capital:,.2f}")
            print(f"💰 Final Balance: ${final_balance:,.2f}")
            print(f"📊 Total Return: {total_return:+.2f}%")
            print(f"🎯 Total Trades: {total_trades}")
            print(f"✅ Winning Trades: {winning_trades}")
            print(f"❌ Losing Trades: {losing_trades}")
            print(f"📊 Win Rate: {win_rate:.1f}%")
            print(f"💵 Average Win: ${avg_win:.2f}")
            print(f"💸 Average Loss: ${avg_loss:.2f}")
            print(f"⚡ Profit Factor: {profit_factor:.2f}")
            
            return {
                'pair': pair_name,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'win_rate': win_rate,
                'total_return': total_return,
                'profit_factor': profit_factor,
                'final_balance': final_balance,
                'trades': trades[-3:]  # Last 3 trades for detail
            }
        else:
            print(f"⚠️ No trades executed for {pair_name}")
            return None
            
    except Exception as e:
        print(f"❌ Error backtesting {pair_name}: {e}")
        return None

def run_full_system_backtest():
    """Run complete system backtest on all pairs with real data"""
    
    print("🚀 COMPREHENSIVE REAL DATA BACKTEST")
    print("=" * 60)
    
    # Real yfinance symbols
    test_pairs = {
        'EURUSD': 'EURUSD=X',
        'GBPJPY': 'GBPJPY=X', 
        'USDJPY': 'USDJPY=X',
        'US30': '^DJI'  # Test subset for speed
    }
    
    results = []
    total_initial = 40000  # $10k per pair
    
    for pair_name, symbol in test_pairs.items():
        result = backtest_real_data(symbol, pair_name, days=14, initial_capital=10000)
        if result:
            results.append(result)
    
    # Portfolio summary
    if results:
        print(f"\n" + "=" * 60)
        print("🏆 PORTFOLIO BACKTEST SUMMARY")
        print("=" * 60)
        
        total_trades = sum(r['total_trades'] for r in results)
        total_winning = sum(r['winning_trades'] for r in results)
        total_final = sum(r['final_balance'] for r in results)
        
        portfolio_return = ((total_final - total_initial) / total_initial) * 100
        overall_win_rate = (total_winning / total_trades) * 100 if total_trades > 0 else 0
        
        print(f"💰 Portfolio Initial: ${total_initial:,.2f}")
        print(f"💰 Portfolio Final: ${total_final:,.2f}")
        print(f"📊 Portfolio Return: {portfolio_return:+.2f}%")
        print(f"🎯 Total Trades: {total_trades}")
        print(f"📊 Overall Win Rate: {overall_win_rate:.1f}%")
        
        print(f"\n📋 PAIR BREAKDOWN:")
        print(f"{'Pair':<8} {'Trades':<7} {'Win%':<6} {'Return%':<8} {'P.Factor':<8}")
        print("-" * 45)
        
        for r in results:
            print(f"{r['pair']:<8} {r['total_trades']:<7} {r['win_rate']:<6.1f} {r['total_return']:<8.1f} {r['profit_factor']:<8.1f}")
        
        print(f"\n🎉 REAL DATA BACKTEST COMPLETE!")
        print(f"✅ System validated with {total_trades} real trades")
        print(f"✅ Portfolio shows {portfolio_return:+.1f}% return")
        
        if portfolio_return > 0:
            print(f"🚀 PROFITABLE SYSTEM CONFIRMED!")
        else:
            print(f"⚠️ System needs optimization")
    
    return results

if __name__ == "__main__":
    # Run comprehensive backtest
    backtest_results = run_full_system_backtest()