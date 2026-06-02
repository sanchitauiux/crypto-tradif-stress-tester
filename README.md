# crypto-tradif-stress-tester
A Python model simulating cascading risk loops between crypto crashes, bank margin calls, and insurance insolvencies.
# Crypto-TradFi Contagion Stress Tester 

An automated risk simulation engine built in Python to model hidden contagion channels between decentralized finance (DeFi) volatility and traditional financial institutions (Banks and Insurance sectors). 

##  The Problem
Regulators frequently evaluate banks and insurance companies in silos. However, as banks accept cryptocurrency as loan collateral and insurers write policies covering digital asset custody, a sudden crypto crash can trigger a simultaneous double-sector shock through unmapped feedback loops.

This project simulates how an initial crypto market drawdown forces programmatic liquidations at banks, dumping massive supply into the open market, causing a secondary price spiral that subsequently triggers catastrophic underwriting claims and insolvencies in the insurance sector.

##  Key Features
*Live Market Shock Ingestion:** Integrates with `yfinance` to extract historical "Black Swan" price data (e.g., the June 13, 2022 market drop).
*Cascading Simulation Engine:** Separately tracks banking Loan-to-Value (LTV) margin thresholds and insurance liquid capital reserves.
*Endogenous Feedback Loop:** Models a secondary market impact factor—the math behind how a bank's defensive asset dumping inflicts cross-sector damage.
*Risk Visualization Dashboard:** Generates dual-axis analytical graphs mapping system breaking points and "Insolvency Zones" using `matplotlib`.

##  System Architecture & Cascade Logic
 *Initial Shock Wave:** Evaluates positions against a sudden market drawdown (e.g., -40%).
 *Banking Node:** Spikes LTV ratios. If LTV exceeds 85%, forced collateral dumping is triggered.
 *Insurance Node:** Calculates increased custodian failures based on market panic, generating gross insurance claims.
 *Contagion Feedback Loop:** The bank’s liquidations re-depreciate asset prices by an additional impact scale, hitting the insurer a second time.

## 📈 Sample Output Visualizations
When running a sweep across a 0% to -60% crash scenario, the model maps the non-linear risk expansion:

*Bank Breaking Point:** Loan-to-Value breaches safe limits dramatically after a -30% drop.
*Insurer Capital Exhaustion:** The "Insolvency Zone" (negative liquid reserves) triggers right around a -15% to -20% overnight drawdown.

# Getting Started
### Requirements
Ensure you have Python 3.14+ installed along with the required analytical libraries:
```bash
pip install yfinance pandas matplotlib
