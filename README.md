# Smart Money Trading Alerts

## ⚠️ IMPORTANT DISCLAIMER
**This software is for educational and research purposes only. It is NOT financial advice. Trading financial instruments involves substantial risk of loss, and you could lose all of your invested capital. Past performance does not guarantee future results. Use this system at your own risk and only trade with capital you can afford to lose. Always consult with a qualified financial advisor before making trading decisions.**

## Project Overview
This project is a comprehensive day trading platform built around Smart Money Concepts (SMC) for real-time market analysis, signal generation, and strategy optimization. It integrates authentic market data from yfinance and provides a live web dashboard for monitoring trading signals and system status.

## Key Features
- **Real Market Data**: 100% live data from yfinance (Yahoo Finance) for 7 trading pairs (6 forex, 1 index)
- **Flask Web Dashboard**: Real-time price display and system status at http://127.0.0.1:5000
- **SMC Pattern Detection**: Advanced algorithms for Fair Value Gaps, Order Blocks, Liquidity Sweeps, Breaker Blocks
- **Day Trading Optimization**: 5-15 minute timeframes, session-aware strategies, dynamic risk management
- **Session Analysis**: Trading session optimizer for London, NY, Tokyo, and overlaps
- **Profitability Analysis**: Historical backtesting and real-time performance metrics
- **Strategy Refinement**: Adjustable parameters for confidence, risk/reward, and trade quality

## Main Components
- `index.py`: Main Flask app serving the web dashboard and live market data
- `day_trading_optimizer.py`: SMC pattern detection and day trading optimization
- `session_optimizer.py`: Trading session analysis and strategy adaptation
- `balanced_strategy.py`: Optimized trading strategy with improved parameters
- `profitability_analysis.py` & `optimized_profitability_test.py`: Backtesting and profitability analysis
- `comprehensive_smc_test.py`: System verification suite
- `final_smc_report.py`: Final system status and operational report
- `web_app/`: Contains web dashboard, deployment scripts, and API integration

## Data Source
- **yfinance 0.2.66**: Unlimited real-time market data for all trading pairs
- **No simulated or fake data**: All analysis and signals are based on authentic market prices

## Trading Logic
- **SMC Patterns**: Detects Fair Value Gaps, Order Blocks, Liquidity Sweeps, Breaker Blocks
- **Signal Generation**: Only high-confidence, high-quality signals are generated (75%+ confidence, 65%+ quality)
- **Risk Management**: 1:3 minimum risk/reward, max 4 trades/day, 0.5-0.6% risk per trade
- **Session Awareness**: Adapts strategy based on active trading session (e.g., Tokyo, London)

## Performance Metrics
- **Current Status**: System is operational, but not yet profitable (-1.15% portfolio return in latest test)
- **Win Rate**: 18.8% (needs improvement)
- **Profit Factor**: 0.03 (should be >1.0 for profitability)
- **Drawdown**: Controlled (<3%)

## How to Use
1. **Start the Flask Web Dashboard**:

2. **Run Real-Time Scanner**:
   ```powershell
   python realtime_day_trading.py
   ```

3. **Test Strategy**:
   ```powershell
   python balanced_strategy.py
   ```

4. **Analyze Profitability**:
   ```powershell
   python optimized_profitability_test.py
   ```

5. **Verify System Status**:
   ```powershell
   python final_smc_report.py
   ```

## Deployment
- **Local**: Run all scripts directly in the root folder
- **Web App**: See `web_app/` for deployment guides and scripts (supports Vercel, manual deployment)

## Limitations & Next Steps
- **Profitability**: Current strategy is not profitable; further refinement needed
- **Signal Quality**: Focus on improving win rate and profit factor
- **Live Trading**: Recommended to use paper trading until strategy is profitable

## ⚠️ Risk Warning
**IMPORTANT**: This trading system is currently showing negative returns (-1.15% portfolio return). Do not use real money until the strategy becomes consistently profitable. Always use proper risk management and never risk more than you can afford to lose.

## Authors & Contributors
- Project Owner: bandasihle

## License
This project is provided "as is" without warranty of any kind. Users assume all responsibility for any trading decisions made using this software.

## Contact
For questions or support, open an issue or contact the project owner.
