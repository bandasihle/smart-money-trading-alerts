#!/usr/bin/env python3
"""
Day Trading Strategy Profitability Analysis
Historical backtesting with REAL market data to measure actual performance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from day_trading_optimizer import DayTradingPatternDetector, DayTradingRiskManager, get_intraday_data
from session_optimizer import TradingSessionOptimizer
from trading_system import DayTradingSmartMoney
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class DayTradingProfitabilityAnalyzer:
    """Comprehensive profitability analysis for day trading strategy"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.detector = DayTradingPatternDetector()
        self.risk_manager = DayTradingRiskManager()
        self.session_optimizer = TradingSessionOptimizer()
        
    def backtest_day_trading_strategy(self, symbol, pair_name, days=30):
        """Backtest day trading strategy on real historical data"""
        
        print(f"\n🔥 BACKTESTING {pair_name} DAY TRADING STRATEGY")
        print("=" * 55)
        
        try:
            # Get high-frequency historical data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{days}d", interval="15m")
            
            if len(data) < 100:
                print(f"❌ Insufficient data for {pair_name}")
                return None
            
            print(f"📊 Data: {len(data)} bars over {days} days")
            print(f"📅 Period: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
            
            # Initialize tracking variables
            trades = []
            daily_returns = []
            equity_curve = [self.initial_capital]
            current_capital = self.initial_capital
            
            # Process data in daily chunks for realistic day trading simulation
            data['date'] = data.index.date
            unique_dates = data['date'].unique()
            
            total_trading_days = len(unique_dates)
            profitable_days = 0
            
            print(f"📈 Simulating {total_trading_days} trading days...")
            
            for date in unique_dates:
                daily_data = data[data['date'] == date].copy()
                
                if len(daily_data) < 10:  # Need minimum bars per day
                    continue
                
                daily_pnl = 0
                daily_trades = 0
                max_daily_trades = 5  # Limit for day trading
                
                # Simulate real-time pattern detection throughout the day
                for i in range(20, len(daily_data), 5):  # Check every 5 bars (75 minutes)
                    if daily_trades >= max_daily_trades:
                        break
                    
                    # Get data up to current point
                    current_data = daily_data.iloc[:i+1]
                    
                    # Detect patterns
                    signals = self.detector.analyze_intraday_patterns(current_data)
                    
                    if signals and len(signals) > 0:
                        # Take the best signal
                        best_signal = max(signals, key=lambda x: x['confidence'])
                        
                        if best_signal['confidence'] >= 70:  # Minimum threshold
                            # Simulate trade execution
                            entry_price = current_data['Close'].iloc[-1]
                            
                            # Calculate position sizing with day trading risk
                            trade_setup = self.risk_manager.calculate_day_trading_position_size(
                                best_signal, entry_price, current_capital
                            )
                            
                            if trade_setup['position_size'] > 0:
                                # Simulate trade outcome using next 1-4 hours of data
                                future_start = i + 1
                                future_end = min(i + 16, len(daily_data))  # Next 4 hours max
                                
                                if future_end > future_start:
                                    future_data = daily_data.iloc[future_start:future_end]
                                    
                                    # Track price vs stop/target levels
                                    trade_pnl = self.simulate_trade_outcome(
                                        best_signal, trade_setup, future_data
                                    )
                                    
                                    # Record trade
                                    trade_record = {
                                        'date': date,
                                        'pair': pair_name,
                                        'direction': best_signal['direction'],
                                        'entry_price': entry_price,
                                        'stop_loss': trade_setup['stop_loss'],
                                        'take_profit': trade_setup['take_profit'],
                                        'position_size': trade_setup['position_size'],
                                        'pnl': trade_pnl,
                                        'pattern': best_signal['pattern'],
                                        'confidence': best_signal['confidence'],
                                        'risk_amount': trade_setup['risk_amount']
                                    }
                                    
                                    trades.append(trade_record)
                                    daily_pnl += trade_pnl
                                    daily_trades += 1
                                    current_capital += trade_pnl
                
                # Record daily performance
                daily_returns.append(daily_pnl)
                equity_curve.append(current_capital)
                
                if daily_pnl > 0:
                    profitable_days += 1
            
            # Calculate performance metrics
            if trades:
                return self.calculate_performance_metrics(
                    trades, daily_returns, equity_curve, pair_name, total_trading_days, profitable_days
                )
            else:
                print(f"⚠️ No trades executed for {pair_name}")
                return None
                
        except Exception as e:
            print(f"❌ Error backtesting {pair_name}: {e}")
            return None
    
    def simulate_trade_outcome(self, signal, trade_setup, future_data):
        """Simulate realistic trade outcome based on future price action"""
        
        entry_price = trade_setup['entry_price']
        stop_loss = trade_setup['stop_loss']
        take_profit = trade_setup['take_profit']
        position_size = trade_setup['position_size']
        
        # Check if stop or target is hit
        for _, bar in future_data.iterrows():
            if signal['direction'] == 'BUY':
                # Check stop loss first (more realistic)
                if bar['Low'] <= stop_loss:
                    # Stop loss hit
                    pnl = (stop_loss - entry_price) * position_size
                    commission = abs(position_size * entry_price * 0.0002)  # 0.02% spread
                    return pnl - commission
                elif bar['High'] >= take_profit:
                    # Take profit hit
                    pnl = (take_profit - entry_price) * position_size
                    commission = abs(position_size * entry_price * 0.0002)
                    return pnl - commission
            else:  # SELL
                if bar['High'] >= stop_loss:
                    # Stop loss hit
                    pnl = (entry_price - stop_loss) * position_size
                    commission = abs(position_size * entry_price * 0.0002)
                    return pnl - commission
                elif bar['Low'] <= take_profit:
                    # Take profit hit
                    pnl = (entry_price - take_profit) * position_size
                    commission = abs(position_size * entry_price * 0.0002)
                    return pnl - commission
        
        # If neither hit, close at end of day (realistic for day trading)
        exit_price = future_data['Close'].iloc[-1]
        if signal['direction'] == 'BUY':
            pnl = (exit_price - entry_price) * position_size
        else:
            pnl = (entry_price - exit_price) * position_size
        
        commission = abs(position_size * entry_price * 0.0002)
        return pnl - commission
    
    def calculate_performance_metrics(self, trades, daily_returns, equity_curve, pair_name, total_days, profitable_days):
        """Calculate comprehensive performance metrics"""
        
        # Basic metrics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['pnl'] > 0])
        losing_trades = total_trades - winning_trades
        
        total_pnl = sum(t['pnl'] for t in trades)
        total_return_pct = (total_pnl / self.initial_capital) * 100
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # PnL analysis
        winning_pnls = [t['pnl'] for t in trades if t['pnl'] > 0]
        losing_pnls = [t['pnl'] for t in trades if t['pnl'] < 0]
        
        avg_win = np.mean(winning_pnls) if winning_pnls else 0
        avg_loss = np.mean(losing_pnls) if losing_pnls else 0
        
        profit_factor = abs(sum(winning_pnls) / sum(losing_pnls)) if losing_pnls else float('inf')
        
        # Risk metrics
        daily_returns_pct = [(ret / self.initial_capital) * 100 for ret in daily_returns]
        max_drawdown = self.calculate_max_drawdown(equity_curve)
        
        sharpe_ratio = self.calculate_sharpe_ratio(daily_returns_pct)
        
        # Day trading specific metrics
        daily_win_rate = (profitable_days / total_days) * 100 if total_days > 0 else 0
        avg_trades_per_day = total_trades / total_days if total_days > 0 else 0
        
        # Display results
        print(f"\n📈 PROFITABILITY RESULTS FOR {pair_name}:")
        print("-" * 45)
        print(f"💰 Initial Capital: ${self.initial_capital:,.2f}")
        print(f"💰 Final Capital: ${self.initial_capital + total_pnl:,.2f}")
        print(f"📊 Total Return: {total_return_pct:+.2f}%")
        print(f"📊 Total P&L: ${total_pnl:+,.2f}")
        
        print(f"\n🎯 TRADING STATISTICS:")
        print(f"   Total Trades: {total_trades}")
        print(f"   Winning Trades: {winning_trades}")
        print(f"   Losing Trades: {losing_trades}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   Trades/Day: {avg_trades_per_day:.1f}")
        
        print(f"\n💵 P&L ANALYSIS:")
        print(f"   Average Win: ${avg_win:.2f}")
        print(f"   Average Loss: ${avg_loss:.2f}")
        print(f"   Profit Factor: {profit_factor:.2f}")
        print(f"   Best Trade: ${max(t['pnl'] for t in trades):.2f}")
        print(f"   Worst Trade: ${min(t['pnl'] for t in trades):.2f}")
        
        print(f"\n📊 RISK METRICS:")
        print(f"   Max Drawdown: {max_drawdown:.2f}%")
        print(f"   Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"   Daily Win Rate: {daily_win_rate:.1f}%")
        
        return {
            'pair': pair_name,
            'total_return_pct': total_return_pct,
            'total_pnl': total_pnl,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'avg_trades_per_day': avg_trades_per_day,
            'daily_win_rate': daily_win_rate,
            'trades': trades[-5:]  # Last 5 trades for detail
        }
    
    def calculate_max_drawdown(self, equity_curve):
        """Calculate maximum drawdown percentage"""
        peak = equity_curve[0]
        max_dd = 0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_dd:
                max_dd = drawdown
        
        return max_dd
    
    def calculate_sharpe_ratio(self, daily_returns):
        """Calculate annualized Sharpe ratio"""
        if len(daily_returns) == 0:
            return 0
        
        avg_return = np.mean(daily_returns)
        std_return = np.std(daily_returns)
        
        if std_return == 0:
            return 0
        
        # Annualized (assuming 252 trading days)
        sharpe = (avg_return / std_return) * np.sqrt(252)
        return sharpe

def run_profitability_analysis():
    """Run comprehensive profitability analysis on multiple pairs"""
    
    print("🚀 DAY TRADING STRATEGY PROFITABILITY ANALYSIS")
    print("=" * 65)
    print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    analyzer = DayTradingProfitabilityAnalyzer(initial_capital=10000)
    
    # Test pairs with good day trading characteristics
    test_pairs = {
        'EURUSD': 'EURUSD=X',
        'GBPJPY': 'GBPJPY=X',
        'USDJPY': 'USDJPY=X',
        'USDCAD': 'USDCAD=X'
    }
    
    results = []
    total_initial = len(test_pairs) * 10000
    
    for pair_name, symbol in test_pairs.items():
        result = analyzer.backtest_day_trading_strategy(symbol, pair_name, days=21)  # 3 weeks
        if result:
            results.append(result)
    
    # Portfolio analysis
    if results:
        print(f"\n" + "=" * 65)
        print("🏆 PORTFOLIO PROFITABILITY SUMMARY")
        print("=" * 65)
        
        total_return = sum(r['total_pnl'] for r in results)
        total_trades = sum(r['total_trades'] for r in results)
        total_winning = sum(r['total_trades'] * r['win_rate'] / 100 for r in results)
        
        portfolio_return_pct = (total_return / total_initial) * 100
        overall_win_rate = (total_winning / total_trades) * 100 if total_trades > 0 else 0
        
        print(f"💰 Portfolio Initial: ${total_initial:,.2f}")
        print(f"💰 Portfolio Final: ${total_initial + total_return:,.2f}")
        print(f"📊 Portfolio Return: {portfolio_return_pct:+.2f}%")
        print(f"📊 Total P&L: ${total_return:+,.2f}")
        print(f"🎯 Total Trades: {total_trades}")
        print(f"📈 Overall Win Rate: {overall_win_rate:.1f}%")
        
        # Calculate portfolio metrics
        avg_profit_factor = np.mean([r['profit_factor'] for r in results if r['profit_factor'] != float('inf')])
        avg_sharpe = np.mean([r['sharpe_ratio'] for r in results])
        max_drawdown = max([r['max_drawdown'] for r in results])
        
        print(f"⚡ Avg Profit Factor: {avg_profit_factor:.2f}")
        print(f"📊 Avg Sharpe Ratio: {avg_sharpe:.2f}")
        print(f"⚠️ Max Drawdown: {max_drawdown:.2f}%")
        
        print(f"\n📋 INDIVIDUAL PAIR PERFORMANCE:")
        print(f"{'Pair':<8} {'Return%':<8} {'Trades':<7} {'Win%':<6} {'P.Factor':<8} {'Sharpe':<7}")
        print("-" * 55)
        
        for r in results:
            pf_display = f"{r['profit_factor']:.1f}" if r['profit_factor'] != float('inf') else "∞"
            print(f"{r['pair']:<8} {r['total_return_pct']:<8.1f} {r['total_trades']:<7} {r['win_rate']:<6.1f} {pf_display:<8} {r['sharpe_ratio']:<7.1f}")
        
        print(f"\n💡 PROFITABILITY INSIGHTS:")
        
        if portfolio_return_pct > 0:
            print(f"✅ PROFITABLE STRATEGY: {portfolio_return_pct:+.1f}% return over 3 weeks")
            
            # Annualized projections
            weekly_return = portfolio_return_pct / 3
            monthly_return = weekly_return * 4.33
            annual_return = weekly_return * 52
            
            print(f"📈 Projected Monthly: {monthly_return:+.1f}%")
            print(f"📈 Projected Annual: {annual_return:+.1f}%")
            
            if avg_profit_factor > 1.5:
                print(f"✅ STRONG PROFIT FACTOR: {avg_profit_factor:.1f} indicates robust edge")
            
            if overall_win_rate > 50:
                print(f"✅ HIGH WIN RATE: {overall_win_rate:.1f}% shows consistent performance")
                
        else:
            print(f"⚠️ STRATEGY NEEDS OPTIMIZATION: {portfolio_return_pct:+.1f}% return")
            print(f"💡 Consider adjusting pattern thresholds or risk parameters")
        
        print(f"\n🎉 ANALYSIS COMPLETE!")
        print(f"📊 Strategy tested with {total_trades} real trades over 21 days")
        
    return results

if __name__ == "__main__":
    # Run profitability analysis
    profitability_results = run_profitability_analysis()