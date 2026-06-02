import yfinance as yf
import pandas as pd

def fetch_market_shock_data():
    print("🛰️ Connecting to Yahoo Finance to fetch historical data...")
    
    # We fetch a 5-year window to capture major market cycles up to 2026
    ticker = "BTC-USD"
    data = yf.download(ticker, start="2021-01-01", end="2026-01-01")
    
    if data.empty:
        print("❌ Error: Could not fetch data. Check your internet connection.")
        return None
        
    # Calculate daily percent change based on the 'Close' price
    data['Daily_Return'] = data['Close'].pct_change()
    
    # Find the single worst drop day in the dataset
    worst_day = data.sort_values(by='Daily_Return').iloc[0]
    worst_date = worst_day.name.strftime('%Y-%m-%d')
    worst_return = worst_day['Daily_Return'].item() # Converts to standard float
    
    print("\n--- HISTORICAL DATA ANALYSIS COMPLETE ---")
    print(f"✅ Successfully loaded {len(data)} days of market data.")
    print(f"🔥 Worst single-day crash found on: {worst_date}")
    print(f"📊 Drop magnitude: {worst_return * 100:.2f}%")
    print("-----------------------------------------\n")
    
    return worst_return

# Test the function
market_shock = fetch_market_shock_data()
# ==========================================
# STEP 2: CORE SIMULATION ENGINE (NODES)
# ==========================================

def simulate_banking_sector(price_drop):
    print("\n---🏦 BANKING SECTOR STRESS ANALYSIS ---")
    
    # Initial setup of a bank holding crypto-collateralized loans
    loan_amount = 50_000_000       # $50M in active loans
    collateral_value = 85_000_000  # Originally backed by $85M in BTC
    
    # Calculate original and post-shock Loan-to-Value (LTV) ratios
    initial_ltv = loan_amount / collateral_value
    post_shock_collateral = collateral_value * (1 + price_drop)
    new_ltv = loan_amount / post_shock_collateral
    
    print(f"Initial Bank LTV: {initial_ltv * 100:.2f}%")
    print(f"Post-Shock Collateral Value: ${post_shock_collateral:,.2f}")
    print(f"New Bank LTV: {new_ltv * 100:.2f}%")
    
    # Define regulatory and risk risk thresholds
    margin_call_threshold = 0.75  # 75% LTV triggers a margin call
    liquidation_threshold = 0.85  # 85% LTV triggers forced asset sell-off
    
    bank_action = "STABLE"
    forced_liquidation_volume = 0.0
    
    if new_ltv >= liquidation_threshold:
        bank_action = "LIQUIDATION"
        print("🚨 CRITICAL: Liquidation threshold breached! Bank is forcibly selling collateral.")
        forced_liquidation_volume = post_shock_collateral
    elif new_ltv >= margin_call_threshold:
        bank_action = "MARGIN_CALL"
        print("⚠️ WARNING: Margin call triggered. Borrowers must post more capital.")
    else:
        print("✅ Bank status remains stable under this shock level.")
        
    return bank_action, forced_liquidation_volume


def simulate_insurance_sector(price_drop):
    print("\n---🛡️ INSURANCE SECTOR STRESS ANALYSIS ---")
    
    # Setup of an insurer covering crypto custody policies
    liquid_capital_reserves = 20_000_000  # Insurer has $20M in cash to pay claims
    total_insured_exposure = 100_000_000  # Insuring $100M total of assets in custody
    
    # Assume market price drop correlates with higher custodian stress/insolvencies
    # We will use the absolute drop value to estimate a claims rate
    implied_claim_rate = abs(price_drop) * 1.5  # Linear risk proxy
    gross_claims = total_insured_exposure * min(implied_claim_rate, 1.0)
    
    # After 5% policyholder deductibles
    net_claims_payout = gross_claims * 0.95
    remaining_capital = liquid_capital_reserves - net_claims_payout
    
    print(f"Expected Claim Rate: {implied_claim_rate * 100:.2f}% of insured custody market")
    print(f"Gross Insurance Claims Filed: ${gross_claims:,.2f}")
    print(f"Net Claims Payout (Post-Deductible): ${net_claims_payout:,.2f}")
    
    insurance_action = "STABLE"
    if remaining_capital < 0:
        insurance_action = "INSOLVENT"
        print(f"🚨 INSURER INSOLVENCY: Capital depleted! Deficit of ${abs(remaining_capital):,.2f}")
    else:
        print(f"✅ Insurer survives with ${remaining_capital:,.2f} in excess capital reserves.")
        
    return insurance_action, net_claims_payout

# ==========================================
# RUNNING THE PIPELINE
# ==========================================
print("\n🔥 RUNNING SYSTEMIC CASCADING STRESS TEST 🔥")

# 1. Feed our real historical worst-day drop into the engine
bank_status, liquidations = simulate_banking_sector(market_shock)
insurer_status, claims_payout = simulate_insurance_sector(market_shock)
# ==========================================
# STEP 3: THE SYSTEMIC FEEDBACK LOOP ENGINE
# ==========================================

def run_cascading_stress_test(initial_shock):
    print("\n=========================================")
    print("🌊 STARTING CASCADING CONTAGION SIMULATION 🌊")
    print("=========================================")
    
    # Track the evolving shock wave
    current_shock = initial_shock
    print(f"Initial Market Shock Wave: {current_shock * 100:.2f}%")
    
    # --- PHASE 1: Run Independent Nodes ---
    bank_status, liquidation_vol = simulate_banking_sector(current_shock)
    insurer_status, net_claims = simulate_insurance_sector(current_shock)
    
    # --- PHASE 2: Calculate Systemic Feedback Loop ---
    # Define a Market Impact Factor: How much extra market drop happens per dollar liquidated
    # For every $10M dumped, the market drops an extra 1% (0.01)
    market_impact_factor = 0.01 / 10_000_000 
    
    secondary_drop = 0.0
    if bank_status == "LIQUIDATION" and liquidation_vol > 0:
        secondary_drop = liquidation_vol * market_impact_factor
        print(f"\n💥 SYSTEMIC CONTAGION IMPACT:")
        print(f"   Bank fire-sold ${liquidation_vol:,.2f} of crypto collateral.")
        print(f"   This forced dumping causes a secondary price drop of: -{secondary_drop * 100:.2f}%")
        
        # Update the shock wave with the compounded damage
        current_shock = current_shock - secondary_drop
        print(f"   📉 Total Compounded Market Drop: {current_shock * 100:.2f}%")
        
        # Re-evaluate the Insurance sector under the secondary stress wave
        print("\n🔄 RE-SHOCKING THE SYSTEM (Feedback Loop hitting Insurer)...")
        insurer_status, net_claims = simulate_insurance_sector(current_shock)
        
    elif bank_status == "MARGIN_CALL":
        # If it's a margin call, borrowers liquidate traditional assets (equities/bonds) to get cash
        traditional_liquidity_drain = 5_000_000 # Borrowers pull out $5M cash
        print(f"\n💧 SYSTEMIC LIQUIDITY DRAIN:")
        print(f"   Borrowers pulled ${traditional_liquidity_drain:,.2f} out of traditional markets to meet margin calls.")
        print(f"   This strains TradFi liquidity pools but didn't trigger a secondary crypto crash.")
        
    print("\n=========================================")
    print("🏁 FINAL SYSTEMIC RISK REPORT")
    print(f"   Bank Status:      {bank_status}")
    print(f"   Insurer Status:   {insurer_status}")
    print(f"   Total Market Drop: {current_shock * 100:.2f}%")
    print("=========================================\n")


# ==========================================
# TEST CASE 1: Run with Real Historical Data (-15.97%)
# ==========================================
print("🧪 TESTING WITH HISTORICAL 2022 BLACK SWAN DATA...")
run_cascading_stress_test(market_shock)

# ==========================================
# TEST CASE 2: Run with an Algorithmic Flash Crash (-40.00%)
# ==========================================
print("\n🧪 TESTING WITH SYSTEMIC FLASH CRASH (-40%)")
run_cascading_stress_test(-0.40)
import matplotlib.pyplot as plt

def plot_stress_test_results():
    print("\n📊 Generating Risk Visualization Charts...")
    
    # We will simulate a range of shocks from 0% to -60% to map out the 'breaking point'
    shocks = [0, -0.10, -0.20, -0.30, -0.40, -0.50, -0.60]
    bank_ltvs = []
    insurer_capitals = []
    
    # Run a quick sweep across the ranges to collect plot data
    for s in shocks:
        # Bank calculations
        post_shock_col = 85_000_000 * (1 + s)
        bank_ltvs.append((50_000_000 / post_shock_col) * 100)
        
        # Insurer calculations
        gross_cl = 100_000_000 * (abs(s) * 1.5)
        net_payout = min(gross_cl, 100_000_000) * 0.95
        insurer_capitals.append((20_000_000 - net_payout) / 1_000_000) # In Millions
        
    # Create a clean side-by-side plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Bank LTV Vulnerability
    ax1.plot([s*100 for s in shocks], bank_ltvs, color='darkblue', marker='o', linewidth=2)
    ax1.axhline(85, color='red', linestyle='--', label='Forced Liquidation Threshold (85%)')
    ax1.set_title("Bank Loan-to-Value (LTV) vs Crypto Crash")
    ax1.set_xlabel("Crypto Market Drop (%)")
    ax1.set_ylabel("Bank LTV (%)")
    ax1.invert_xaxis()
    ax1.legend()
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Plot 2: Insurance Capital Depletion
    ax2.plot([s*100 for s in shocks], insurer_capitals, color='crimson', marker='s', linewidth=2)
    ax2.axhline(0, color='black', linestyle='-', linewidth=1.5)
    ax2.fill_between([s*100 for s in shocks], insurer_capitals, 0, where=[c < 0 for c in insurer_capitals], color='red', alpha=0.2, label='Insolvency Zone')
    ax2.set_title("Insurer Capital Reserves vs Crypto Crash")
    ax2.set_xlabel("Crypto Market Drop (%)")
    ax2.set_ylabel("Liquid Capital Reserves ($ Millions)")
    ax2.invert_xaxis()
    ax2.legend()
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    print("📈 Displaying graphs. Close the graph window to finish the program.")
    plt.show()

# Run the visualization tool
plot_stress_test_results()
