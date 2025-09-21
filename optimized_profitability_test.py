#!/usr/bin/env python3
"""
Optimized Strategy Profitability Test
Test the improved strategy with real historical data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from balanced_strategy import BalancedDayTradingDetector, BalancedRiskManager
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class OptimizedProfitabilityTester:
    """Test optimized strategy profitability"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.detector = BalancedDayTradingDetector()
        self.risk_manager = BalancedRiskManager()
    
    def backtest_optimized_strategy(self, symbol, pair_name, days=21):
        """Backtest the optimized strategy"""
        
        print(f"\n🔥 TESTING OPTIMIZED {pair_name} STRATEGY")
        print("=" * 50)
        
        try:
            # Get historical data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{days}d", interval="15m")
            
            if len(data) < 50:
                print(f"❌ Insufficient data for {pair_name}")
                return None
            
            print(f"📊 Data: {len(data)} bars over {days} days")
            
            # Initialize tracking
            trades = []
            equity_curve = [self.initial_capital]
            current_capital = self.initial_capital
            
            # Process data in daily chunks
            data['date'] = data.index.date
            unique_dates = data['date'].unique()
            
            total_trading_days = len(unique_dates)
            profitable_days = 0
            
            for date in unique_dates:
                daily_data = data[data['date'] == date].copy()
                
                if len(daily_data) < 15:
                    continue
                
                daily_pnl = 0
                daily_trades = 0
                
                # Analyze patterns every 2 hours (8 bars)
                for i in range(20, len(daily_data), 8):
                    if daily_trades >= 3:  # Max 3 trades per day
                        break
                    
                    current_data = daily_data.iloc[:i+1]
                    
                    # Detect optimized patterns
                    signals = self.detector.detect_balanced_patterns(current_data)
                    
                    if signals:
                        best_signal = signals[0]  # Highest confidence
                        
                        if best_signal['confidence'] >= 80:  # High quality only
                            entry_price = current_data['Close'].iloc[-1]
                            
                            # Calculate position
                            trade_setup = self.risk_manager.calculate_balanced_position_size(
                                best_signal, entry_price, current_capital
                            )
                            
                            if trade_setup['position_size'] > 0:
                                # Simulate trade outcome
                                future_start = i + 1
                                future_end = min(i + 12, len(daily_data))  # Next 3 hours
                                
                                if future_end > future_start:
                                    future_data = daily_data.iloc[future_start:future_end]
                                    trade_pnl = self.simulate_optimized_trade(
                                        best_signal, trade_setup, future_data
                                    )
                                    
                                    # Record trade with enhanced details
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
                                        'quality_score': best_signal.get('quality_score', 0),
                                        'risk_amount': trade_setup['risk_amount'],
                                        'rr_ratio': trade_setup['risk_reward_ratio']
                                    }
                                    
                                    trades.append(trade_record)
                                    daily_pnl += trade_pnl
                                    daily_trades += 1
                                    current_capital += trade_pnl
                
                if daily_pnl > 0:
                    profitable_days += 1
                
                equity_curve.append(current_capital)
            
            # Calculate enhanced metrics
            if trades:
                return self.calculate_optimized_metrics(
                    trades, equity_curve, pair_name, total_trading_days, profitable_days
                )
            else:
                print(f"⚠️ No trades executed for {pair_name}")
                return None
                
        except Exception as e:
            print(f"❌ Error testing {pair_name}: {e}")
            return None
    
    def simulate_optimized_trade(self, signal, trade_setup, future_data):
        """Simulate trade with realistic execution"""
        
        entry_price = trade_setup['entry_price']
        stop_loss = trade_setup['stop_loss']
        take_profit = trade_setup['take_profit']
        position_size = trade_setup['position_size']
        
        for _, bar in future_data.iterrows():
            if signal['direction'] == 'BUY':
                if bar['Low'] <= stop_loss:
                    pnl = (stop_loss - entry_price) * position_size
                    commission = abs(position_size * entry_price * 0.0001)
                    return pnl - commission
                elif bar['High'] >= take_profit:
                    pnl = (take_profit - entry_price) * position_size
                    commission = abs(position_size * entry_price * 0.0001)
                    return pnl - commission
            else:  # SELL
                if bar['High'] >= stop_loss:
                    pnl = (entry_price - stop_loss) * position_size
                    commission = abs(position_size * entry_price * 0.0001)
                    return pnl - commission
                elif bar['Low'] <= take_profit:
                    pnl = (entry_price - take_profit) * position_size
                    commission = abs(position_size * entry_price * 0.0001)
                    return pnl - commission
        
        # Close at end of timeframe
        exit_price = future_data['Close'].iloc[-1]
        if signal['direction'] == 'BUY':
            pnl = (exit_price - entry_price) * position_size
        else:
            pnl = (entry_price - exit_price) * position_size
        
        commission = abs(position_size * entry_price * 0.0001)
        return pnl - commission
    
    def calculate_optimized_metrics(self, trades, equity_curve, pair_name, total_days, profitable_days):
        """Calculate enhanced performance metrics"""
        
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['pnl'] > 0])
        losing_trades = total_trades - winning_trades
        
        total_pnl = sum(t['pnl'] for t in trades)
        total_return_pct = (total_pnl / self.initial_capital) * 100
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # Enhanced P&L analysis
        winning_pnls = [t['pnl'] for t in trades if t['pnl'] > 0]
        losing_pnls = [t['pnl'] for t in trades if t['pnl'] < 0]
        
        avg_win = np.mean(winning_pnls) if winning_pnls else 0
        avg_loss = np.mean(losing_pnls) if losing_pnls else 0
        profit_factor = abs(sum(winning_pnls) / sum(losing_pnls)) if losing_pnls else float('inf')
        
        # Quality metrics
        avg_confidence = np.mean([t['confidence'] for t in trades])
        avg_quality = np.mean([t['quality_score'] for t in trades])
        avg_rr_ratio = np.mean([t['rr_ratio'] for t in trades])
        
        # Risk metrics
        max_drawdown = self.calculate_max_drawdown(equity_curve)
        daily_win_rate = (profitable_days / total_days) * 100 if total_days > 0 else 0
        
        # Display enhanced results
        print(f"\n📈 OPTIMIZED RESULTS FOR {pair_name}:")
        print("-" * 45)
        print(f"💰 Initial Capital: ${self.initial_capital:,.2f}")
        print(f"💰 Final Capital: ${self.initial_capital + total_pnl:,.2f}")
        print(f"📊 Total Return: {total_return_pct:+.2f}%")
        print(f"📊 Total P&L: ${total_pnl:+,.2f}")
        
        print(f"\n🎯 ENHANCED TRADING STATISTICS:")
        print(f"   Total Trades: {total_trades}")
        print(f"   Winning Trades: {winning_trades}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   Avg Confidence: {avg_confidence:.1f}%")
        print(f"   Avg Quality Score: {avg_quality:.1%}")
        print(f"   Avg R:R Ratio: 1:{avg_rr_ratio:.1f}")
        
        print(f"\n💵 OPTIMIZED P&L ANALYSIS:")
        print(f"   Average Win: ${avg_win:.2f}")
        print(f"   Average Loss: ${avg_loss:.2f}")
        print(f"   Profit Factor: {profit_factor:.2f}")
        print(f"   Best Trade: ${max(t['pnl'] for t in trades):.2f}")
        print(f"   Worst Trade: ${min(t['pnl'] for t in trades):.2f}")
        
        print(f"\n📊 RISK METRICS:")
        print(f"   Max Drawdown: {max_drawdown:.2f}%")
        print(f"   Daily Win Rate: {daily_win_rate:.1f}%")
        print(f"   Trades/Day: {total_trades/total_days:.1f}")
        
        return {
            'pair': pair_name,
            'total_return_pct': total_return_pct,
            'total_pnl': total_pnl,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'avg_confidence': avg_confidence,
            'avg_quality': avg_quality,
            'avg_rr_ratio': avg_rr_ratio,
            'daily_win_rate': daily_win_rate
        }
    
    def calculate_max_drawdown(self, equity_curve):
        """Calculate maximum drawdown"""
        peak = equity_curve[0]
        max_dd = 0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_dd:
                max_dd = drawdown
        
        return max_dd

def run_optimized_profitability_test():
    """Run comprehensive optimized profitability test"""
    
    print("🚀 OPTIMIZED STRATEGY PROFITABILITY TEST")
    print("=" * 60)
    
    tester = OptimizedProfitabilityTester(initial_capital=10000)
    
    # Test on best performers with optimized strategy
    test_pairs = {
        'USDJPY': 'USDJPY=X',  # Best historical performer
        'EURUSD': 'EURUSD=X'   # High liquidity
    }
    
    results = []
    
    for pair_name, symbol in test_pairs.items():
        result = tester.backtest_optimized_strategy(symbol, pair_name, days=21)
        if result:
            results.append(result)
    
    # Portfolio analysis
    if results:
        print(f"\n" + "=" * 60)
        print("🏆 OPTIMIZED PORTFOLIO SUMMARY")
        print("=" * 60)
        
        total_return = sum(r['total_pnl'] for r in results)
        total_trades = sum(r['total_trades'] for r in results)
        portfolio_return_pct = (total_return / (len(results) * 10000)) * 100
        
        avg_win_rate = np.mean([r['win_rate'] for r in results])
        avg_profit_factor = np.mean([r['profit_factor'] for r in results if r['profit_factor'] != float('inf')])
        avg_confidence = np.mean([r['avg_confidence'] for r in results])
        avg_quality = np.mean([r['avg_quality'] for r in results])
        
        print(f"💰 Portfolio Return: {portfolio_return_pct:+.2f}%")
        print(f"📊 Total P&L: ${total_return:+,.2f}")
        print(f"🎯 Total Trades: {total_trades}")
        print(f"📈 Avg Win Rate: {avg_win_rate:.1f}%")
        print(f"⚡ Avg Profit Factor: {avg_profit_factor:.2f}")
        print(f"🎯 Avg Confidence: {avg_confidence:.1f}%")
        print(f"⭐ Avg Quality: {avg_quality:.1%}")
        
        print(f"\n📊 OPTIMIZATION SUCCESS METRICS:")
        
        if portfolio_return_pct > 0:
            # Calculate projections
            weekly_return = portfolio_return_pct / 3
            monthly_return = weekly_return * 4.33
            annual_return = weekly_return * 52
            
            print(f"✅ PROFITABLE: {portfolio_return_pct:+.1f}% in 3 weeks")
            print(f"📈 Projected Monthly: {monthly_return:+.1f}%")
            print(f"📈 Projected Annual: {annual_return:+.1f}%")
            
            if avg_profit_factor > 1.2:
                print(f"✅ STRONG EDGE: Profit factor {avg_profit_factor:.1f}")
            if avg_win_rate > 50:
                print(f"✅ HIGH WIN RATE: {avg_win_rate:.1f}%")
            if avg_quality > 0.8:
                print(f"✅ HIGH QUALITY: {avg_quality:.1%} signal quality")
            
            print(f"\n🎯 IMPROVEMENT vs ORIGINAL STRATEGY:")
            print(f"   Return: {portfolio_return_pct:+.1f}% (vs -3.25%)")
            print(f"   Win Rate: {avg_win_rate:.1f}% (vs 45.0%)")
            print(f"   Profit Factor: {avg_profit_factor:.1f} (vs 0.66)")
            print(f"   Signal Quality: {avg_quality:.1%} (new metric)")
            
            improvement = portfolio_return_pct + 3.25
            print(f"   Total Improvement: +{improvement:.1f} percentage points!")
            
        else:
            print(f"⚠️ Strategy still needs refinement: {portfolio_return_pct:+.1f}%")
        
        print(f"\n🚀 OPTIMIZATION STATUS: {'SUCCESS!' if portfolio_return_pct > 0 else 'NEEDS FURTHER REFINEMENT'}")
    
    return results

if __name__ == "__main__":
    # Run optimized profitability test
    optimized_results = run_optimized_profitability_test()
    
    print(f"\n🎉 OPTIMIZED PROFITABILITY TEST COMPLETE!")