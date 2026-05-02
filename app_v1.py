import streamlit as st

st.set_page_config(page_title="Clarity Investments", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1a1f36; font-weight: 600; }
    h2, h3 { color: #2d3748; font-weight: 500; }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 8px;
        padding: 12px 24px; font-size: 16px; font-weight: 500;
        transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    [data-testid="stMetricValue"] { font-size: 28px; color: #1a1f36; }
    .stAlert { border-radius: 8px; border-left: 4px solid; }
    .streamlit-expanderHeader {
        background-color: #f7fafc; border-radius: 8px; font-weight: 500;
    }
    .action-card {
        background: white; padding: 24px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 16px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = 'loss'
if 'portfolio_allocation' not in st.session_state:
    st.session_state.portfolio_allocation = {'stocks': 70, 'bonds': 30}

market_context = {
    "uncertainty_level": "High",
    "sp500_change": -2.1,
    "tech_sector_change": -5.8,
    "bond_yield": 4.5,
    "market_trend": "down",
    "news_headline": "Federal Reserve signals continued rate hikes amid inflation concerns"
}

def calculate_portfolio(amount, stocks_pct, bonds_pct, demo_mode='loss'):
    total_stocks = int(amount * stocks_pct / 100)
    total_bonds = int(amount * bonds_pct / 100)
    
    if demo_mode == 'loss':
        stock_changes = {"Microsoft": -0.062, "Google": -0.041, "Tesla": -0.123, "S&P 500 Index Fund": -0.053}
        bond_changes = {"US Treasury Bonds": 0.015, "Corporate Bond Fund": 0.008}
    else:
        stock_changes = {"Microsoft": 0.048, "Google": 0.035, "Tesla": 0.092, "S&P 500 Index Fund": 0.041}
        bond_changes = {"US Treasury Bonds": 0.005, "Corporate Bond Fund": 0.003}
    
    holdings = {}
    stock_allocation = {"Microsoft": 0.30, "Google": 0.20, "Tesla": 0.20, "S&P 500 Index Fund": 0.30}
    for stock, pct in stock_allocation.items():
        value = int(total_stocks * pct)
        change = int(value * stock_changes[stock])
        holdings[stock] = {"value": value, "change": change, "percent": stock_changes[stock] * 100}
    
    bond_allocation = {"US Treasury Bonds": 0.70, "Corporate Bond Fund": 0.30}
    for bond, pct in bond_allocation.items():
        value = int(total_bonds * pct)
        change = int(value * bond_changes[bond])
        holdings[bond] = {"value": value, "change": change, "percent": bond_changes[bond] * 100}
    
    return holdings, total_stocks, total_bonds

def apply_portfolio_change(new_stocks_pct, new_bonds_pct):
    st.session_state.portfolio_allocation = {'stocks': new_stocks_pct, 'bonds': new_bonds_pct}
    return True

current_stocks_pct = st.session_state.portfolio_allocation['stocks']
current_bonds_pct = st.session_state.portfolio_allocation['bonds']

if st.session_state.get('onboarded', False) and 'investment_amount' in st.session_state:
    portfolio_value = st.session_state.get('investment_amount', 50000)
else:
    portfolio_value = 50000

portfolio_holdings, total_stocks, total_bonds = calculate_portfolio(
    portfolio_value, current_stocks_pct, current_bonds_pct, st.session_state.demo_mode
)

stocks_change = sum(h["change"] for name, h in portfolio_holdings.items() if "Bond" not in name)
bonds_change = sum(h["change"] for name, h in portfolio_holdings.items() if "Bond" in name)
change_today = stocks_change + bonds_change
previous_value = portfolio_value - change_today
percent_change = (change_today / previous_value) * 100 if previous_value > 0 else 0


# WELCOME SCREEN
if st.session_state.page == 'welcome':
    st.title("Welcome to Clarity Investments")
    st.write("---")
    st.markdown("### Portfolio management made simple")
    st.write("We help everyday investors make confident decisions — whether you're just starting out or navigating market uncertainty.")
    st.write("")
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### I'm new here")
        st.write("Let's set up your first portfolio together. Takes 2 minutes.")
        if st.button("Get Started", use_container_width=True, key="new_user"):
            st.session_state.page = 'onboarding'
            st.session_state.onboard_step = 1
            st.rerun()
    
    with col2:
        st.markdown("#### I already have a portfolio")
        st.write("Skip to your dashboard and see how your investments are doing.")
        if st.button("Go to Dashboard", use_container_width=True, key="existing_user"):
            st.session_state.onboarded = True
            st.session_state.page = 'home'
            st.rerun()

# ONBOARDING
elif st.session_state.page == 'onboarding':
    st.title("Let's build your portfolio")
    st.write("Answer 3 quick questions. No finance jargon, we promise.")
    st.write("---")
    
    if st.session_state.get('onboard_step', 1) == 1:
        st.markdown("### Question 1 of 3: How much do you want to invest?")
        st.write("You can always add more later.")
        amount = st.number_input("Investment Amount ($)", min_value=1000, max_value=1000000, value=50000, step=1000)
        st.write("")
        if st.button("Next", use_container_width=True):
            st.session_state.investment_amount = amount
            st.session_state.onboard_step = 2
            st.rerun()
    
    elif st.session_state.get('onboard_step', 1) == 2:
        st.markdown("### Question 2 of 3: When do you need this money?")
        st.write("This helps us balance growth vs. safety.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Soon (less than 3 years)", use_container_width=True):
                st.session_state.onboard_timeline = 'short'
                st.session_state.onboard_step = 3
                st.rerun()
        with col2:
            if st.button("Medium term (3-10 years)", use_container_width=True):
                st.session_state.onboard_timeline = 'medium'
                st.session_state.onboard_step = 3
                st.rerun()
        with col3:
            if st.button("Long term (10+ years)", use_container_width=True):
                st.session_state.onboard_timeline = 'long'
                st.session_state.onboard_step = 3
                st.rerun()
        st.write("")
        if st.button("Back", use_container_width=True):
            st.session_state.onboard_step = 1
            st.rerun()
    
    elif st.session_state.get('onboard_step', 1) == 3:
        st.markdown("### Question 3 of 3: How would you feel if your investment dropped 15% in a month?")
        st.write("Be honest — there's no wrong answer.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("I'd panic and want to sell", use_container_width=True):
                st.session_state.onboard_comfort = 'low'
                st.session_state.onboard_step = 4
                st.rerun()
        with col2:
            if st.button("I'd be worried but would hold", use_container_width=True):
                st.session_state.onboard_comfort = 'medium'
                st.session_state.onboard_step = 4
                st.rerun()
        with col3:
            if st.button("I'd be fine, markets recover", use_container_width=True):
                st.session_state.onboard_comfort = 'high'
                st.session_state.onboard_step = 4
                st.rerun()
        st.write("")
        if st.button("Back", use_container_width=True):
            st.session_state.onboard_step = 2
            st.rerun()
    
    elif st.session_state.get('onboard_step', 1) == 4:
        st.markdown("### Your starting portfolio")
        timeline = st.session_state.get('onboard_timeline', 'medium')
        comfort = st.session_state.get('onboard_comfort', 'medium')
        amount = st.session_state.get('investment_amount', 50000)
        
        if comfort == 'low' or timeline == 'short':
            stocks = 40
            bonds = 60
            description = "conservative (more stability, less volatility)"
        elif comfort == 'high' and timeline == 'long':
            stocks = 80
            bonds = 20
            description = "growth-focused (more potential returns, more ups and downs)"
        else:
            stocks = 60
            bonds = 40
            description = "balanced (mix of growth and stability)"
        
        stocks_amount = int(amount * stocks / 100)
        bonds_amount = int(amount * bonds / 100)
        
        st.write(f"Based on your answers, we recommend a **{description}** portfolio:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Stocks (Growth)", f"{stocks}%", f"${stocks_amount:,}")
            st.caption("Companies like Apple, Microsoft, index funds")
        with col2:
            st.metric("Bonds (Stability)", f"{bonds}%", f"${bonds_amount:,}")
            st.caption("Government and corporate bonds")
        
        st.write("---")
        
        with st.expander("Why this mix?"):
            if stocks > 60:
                st.write(f"**Why more stocks:** You have a {timeline}-term timeline and feel comfortable with market swings. Stocks historically grow more over time.")
            elif bonds > 60:
                st.write(f"**Why more bonds:** With a {timeline}-term timeline, you need stability. Bonds are safer when you need money soon.")
            else:
                st.write("**Why balanced:** This gives you growth potential while protecting against big drops. It's a great starting point.")
            
            potential_stock_loss = int(stocks_amount * 0.20)
            potential_bond_impact = int(bonds_amount * 0.01)
            net_loss = potential_stock_loss - potential_bond_impact
            
            potential_stock_gain = int(stocks_amount * 0.15)
            potential_bond_gain = int(bonds_amount * 0.02)
            net_gain = potential_stock_gain + potential_bond_gain
            
            st.write(f"**What this means:** If the stock market has a bad year (-20%), your stocks might lose ${potential_stock_loss:,}, but your bonds would likely stay steady or gain slightly (+${potential_bond_impact:,}).")
            st.write("")
            st.write(f"Net impact: around ${net_loss:,} loss.")
            st.write("")
            st.write(f"If the market has a great year (+15%), your stocks might gain ${potential_stock_gain:,}, plus bond gains (+${potential_bond_gain:,}).")
            st.write("")
            st.write(f"Net gain: around ${net_gain:,}.")
            st.write("")
            st.write("**You can adjust this anytime** as markets change or your life changes.")
            
            
        st.write("---")
        st.success("Your portfolio is ready!")
        
        if st.button("Go to Dashboard", use_container_width=True):
            st.session_state.onboarded = True
            st.session_state.portfolio_allocation = {'stocks': stocks, 'bonds': bonds}
            st.session_state.page = 'home'
            st.rerun()

# HOME SCREEN
elif st.session_state.page == 'home':
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("Clarity Investments")
    with col3:
        if st.button(f"Demo: Switch to {'Gain' if st.session_state.demo_mode == 'loss' else 'Loss'} Scenario"):
            st.session_state.demo_mode = 'gain' if st.session_state.demo_mode == 'loss' else 'loss'
            st.rerun()
    
    st.metric(label="Your Portfolio", value=f"${portfolio_value:,}", delta=f"{change_today:,} ({percent_change:.1f}%)")
    st.write(f"**Current Allocation:** {current_stocks_pct}% Stocks (${total_stocks:,}) | {current_bonds_pct}% Bonds (${total_bonds:,})")
    
    st.caption(f"Market News: {market_context['news_headline']}")
    st.caption(f"Market Context: S&P 500 {market_context['sp500_change']:+.1f}% | Tech Sector {market_context['tech_sector_change']:+.1f}% | Uncertainty: {market_context['uncertainty_level']}")
    
    if change_today < 0:
        st.warning(f"Your portfolio dropped {abs(percent_change):.1f}% today, driven primarily by tech stock weakness (Microsoft {portfolio_holdings['Microsoft']['percent']:.1f}%, Tesla {portfolio_holdings['Tesla']['percent']:.1f}%). Markets typically recover within 18 months.")
    elif change_today > 0:
        st.success(f"Great news! Your portfolio gained ${abs(change_today):,} today")
    else:
        st.info("The market favors the disciplined. Stay on the path. Have a nice day.")
    
    st.write("---")
    st.subheader("What would you like to do?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("#### Take me to Safety")
        st.write("Reduce risk during market uncertainty")
        if st.button("View Options", use_container_width=True, key="safety_btn"):
            st.session_state.page = 'safety'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("#### Show Actual Impact")
        st.write("See how each holding is performing")
        if st.button("View Breakdown", use_container_width=True, key="impact_btn"):
            st.session_state.page = 'impact'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col3:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("#### What are my Options?")
        st.write("Explore scenarios and get recommendations")
        if st.button("Explore Scenarios", use_container_width=True, key="scenarios_btn"):
            st.session_state.page = 'scenarios'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
# SAFETY PATH
elif st.session_state.page == 'safety':
    st.write("---")
    st.subheader("Take me to Safety")
    st.write("**We've created a safer version of your portfolio based on current market conditions.**")
    
    safer_stocks = 50
    safer_bonds = 50
    amount_to_move = int((current_stocks_pct - safer_stocks) * portfolio_value / 100)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Current Portfolio**")
        st.write(f"**{current_stocks_pct}% Stocks** (${total_stocks:,})")
        st.write(f"**{current_bonds_pct}% Bonds** (${total_bonds:,})")
    with col2:
        st.write(f"**Recommended (Safer)**")
        st.write(f"**{safer_stocks}% Stocks** (${int(portfolio_value * safer_stocks / 100):,})")
        st.write(f"**{safer_bonds}% Bonds** (${int(portfolio_value * safer_bonds / 100):,})")
    
    st.write("---")
    st.markdown("### Quick Summary")
    if amount_to_move > 0:
        st.write(f"**Move ${amount_to_move:,} from stocks to bonds** to reduce risk in current volatile conditions.")
    
    with st.expander("Why are we recommending this?"):
        st.write(f"**Market Analysis:** Current uncertainty is elevated. Tech stocks (which make up ${total_stocks - portfolio_holdings['S&P 500 Index Fund']['value']:,} of your portfolio) are down {market_context['tech_sector_change']:.1f}% today.")
        st.write(f"**Your Holdings:** Microsoft lost ${abs(portfolio_holdings['Microsoft']['change']):,} today, Tesla lost ${abs(portfolio_holdings['Tesla']['change']):,}. Meanwhile, your bonds gained ${bonds_change:,}.")
        st.write(f"**Why Bonds Now:** The Federal Reserve is raising interest rates to combat inflation. This typically hurts stocks in the short term but makes bonds more attractive. With bond interest rates at {market_context['bond_yield']}%, bonds are offering decent returns with much lower volatility.")
        st.write(f"**Trade-off:** If the market rebounds quickly, you'll capture less upside. But given current conditions, stability matters more.")
        st.write("**Cost:** Platform rebalancing fee: $12 per transaction")
    
    st.write("---")
    st.markdown("### What if the market drops another 20%?")
    
    col1, col2 = st.columns(2)
    current_loss = int(total_stocks * 0.20)
    safer_loss = int(portfolio_value * safer_stocks / 100 * 0.20)
    
    with col1:
        st.metric("Current Portfolio Impact", f"-${current_loss:,}", delta="-20% on stocks", delta_color="inverse")
    with col2:
        st.metric("Safer Portfolio Impact", f"-${safer_loss:,}", delta="-20% on stocks", delta_color="inverse")
    
    st.success(f"The safer portfolio loses ${current_loss - safer_loss:,} less in a continued downturn.")
    st.info(f"This suggestion is based on current market uncertainty and your tech-heavy allocation.")
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Apply this change", use_container_width=True):
            apply_portfolio_change(safer_stocks, safer_bonds)
            st.success("Portfolio updated! Your allocation is now 50% stocks, 50% bonds.")
            st.balloons()
    with col2:
        if st.button("Go back", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# IMPACT PATH
elif st.session_state.page == 'impact':
    st.write("---")
    st.subheader("Show Actual Impact")
    st.write("Here's how your portfolio is performing today:")
    st.markdown("**By Category:**")
    
    stocks_percent_change = (stocks_change / total_stocks) * 100 if total_stocks > 0 else 0
    bonds_percent_change = (bonds_change / total_bonds) * 100 if total_bonds > 0 else 0
    
    with st.expander(f"Stocks: ${stocks_change:,} ({stocks_percent_change:+.1f}%) - Click to see details"):
        st.write("**Individual Stock Holdings:**")
        for name, data in portfolio_holdings.items():
            if "Bond" not in name:
                st.write(f"• {name}: ${data['change']:,} ({data['percent']:+.1f}%)")
        
        if st.session_state.demo_mode == 'loss':
            st.write(f"\n**Why the drop:** The tech sector is down {market_context['tech_sector_change']:.1f}% today. The Federal Reserve raised interest rates to slow inflation, which typically causes investors to sell growth stocks (like tech companies) in the short term and move to safer investments.")
        else:
            st.write(f"\n**Why the gain:** The tech sector is up today. Positive market sentiment and strong earnings reports are driving growth stocks higher.")
    
    with st.expander(f"Bonds: ${bonds_change:,} ({bonds_percent_change:+.1f}%) - Click to see details"):
        st.write("**Individual Bond Holdings:**")
        for name, data in portfolio_holdings.items():
            if "Bond" in name:
                st.write(f"• {name}: ${data['change']:,} ({data['percent']:+.1f}%)")
        
        if st.session_state.demo_mode == 'loss':
            st.write(f"\n**Why the gain:** When stock markets become uncertain, investors often move money into bonds for safety. Additionally, bond interest rates are at {market_context['bond_yield']}%, which is attractive compared to recent years.")
        else:
            st.write(f"\n**Why the modest gain:** Bonds provide steady returns through interest payments, even when stocks are doing well.")
    
    st.write("---")
    
    if st.session_state.demo_mode == 'loss':
        st.info(f"**Summary:** Your tech stocks are down today due to a market-wide tech selloff (uncertainty is high), but bonds are holding steady as investors seek safety. This is normal during periods of market volatility.")
    else:
        st.info(f"**Summary:** Your tech stocks are performing well today, benefiting from positive market momentum. Your bonds continue to provide stable returns through interest payments.")
    
    if st.button("Go back to home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# SCENARIOS PATH
elif st.session_state.page == 'scenarios':
    st.write("---")
    st.subheader("What are my options?")
    st.write("**Tell us what you're thinking about, and we'll show you how to adjust your portfolio based on current market conditions.**")
    
    st.markdown("### What are you worried about or planning for?")
    st.markdown("**Recommended if you're unsure:**")
    if st.button("I'm not sure - Guide me through this", use_container_width=True, key="guide_highlighted"):
        st.session_state.scenario = 'guide_me'
        st.session_state.guide_step = 1
    
    st.write("---")
    st.markdown("**Or choose a specific scenario:**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Market might crash", use_container_width=True):
            st.session_state.scenario = 'crash'
        if st.button("I need cash in 1-2 years", use_container_width=True):
            st.session_state.scenario = 'cash_soon'
        if st.button("Inflation staying high", use_container_width=True):
            st.session_state.scenario = 'inflation'
    with col2:
        if st.button("Saving for big purchase", use_container_width=True):
            st.session_state.scenario = 'big_purchase'
        if st.button("I need consistent returns", use_container_width=True):
            st.session_state.scenario = 'consistent'
    
    st.write("---")
    
    # SCENARIO RECOMMENDATIONS
    if 'scenario' in st.session_state:
        
        if st.session_state.scenario == 'crash':
            st.markdown("### Scenario: Market might crash")
            rec_stocks = 50
            rec_bonds = 50
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Current:** {current_stocks_pct}% Stocks, {current_bonds_pct}% Bonds")
            with col2:
                st.write(f"**Recommended:** {rec_stocks}% Stocks, {rec_bonds}% Bonds")
            
            with st.expander("Why this recommendation?"):
                st.write(f"**Current Market:** Uncertainty is elevated. S&P 500 is down {market_context['sp500_change']:.1f}% today. Tech sector (your largest exposure) is down {market_context['tech_sector_change']:.1f}%.")
                st.write(f"**Your Portfolio:** Tesla is your most volatile holding ({portfolio_holdings['Tesla']['percent']:.1f}% today). Microsoft and Google are also down. Total tech exposure: ${total_stocks - portfolio_holdings['S&P 500 Index Fund']['value']:,}.")
                st.write(f"**Why Move to Bonds:** Your bonds are UP today (+${bonds_change:,}) while stocks are down. This pattern (investors moving to safety) suggests more volatility ahead.")
                st.write(f"**Trade-off:** If markets stabilize quickly, you'll miss some rebound gains.")
                st.write("**Cost:** Platform rebalancing fee: $12")
            
            crash_loss_current = int(total_stocks * 0.30)
            crash_loss_rec = int(portfolio_value * rec_stocks / 100 * 0.30)
            st.write(f"**If market drops 30%:** Current portfolio: -${crash_loss_current:,} | Recommended: -${crash_loss_rec:,}")
            
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Apply this change", use_container_width=True, key="apply_crash"):
                    apply_portfolio_change(rec_stocks, rec_bonds)
                    st.success(f"Portfolio updated to {rec_stocks}% stocks, {rec_bonds}% bonds!")
                    st.balloons()
            with col2:
                if st.button("Go back", use_container_width=True, key="back_crash"):
                    st.session_state.page = 'scenarios'
                    del st.session_state.scenario
                    st.rerun()
        
        elif st.session_state.scenario == 'cash_soon':
            st.markdown("### Scenario: I need cash in 1-2 years")
            rec_stocks = 30
            rec_bonds = 70
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Current:** {current_stocks_pct}% Stocks, {current_bonds_pct}% Bonds")
            with col2:
                st.write(f"**Recommended:** {rec_stocks}% Stocks, {rec_bonds}% Bonds")
            
            with st.expander("Why this recommendation?"):
                st.write(f"**Your Risk:** You're {current_stocks_pct}% in stocks. With current volatility, stocks could drop 20%+ before you need the money.")
                st.write(f"**Today's Proof:** Your stocks lost ${abs(stocks_change):,} in ONE day. If you needed to withdraw today, you'd lock in those losses.")
                st.write(f"**Bonds Are Safer:** Your bonds gained ${bonds_change:,} today. With interest rates at {market_context['bond_yield']}%, you're getting decent returns without the volatility.")
                st.write("**Trade-off:** Lower growth for the next 2 years, but you protect your principal when you need it.")
                st.write("**Cost:** Platform rebalancing fee: $12")
            
            st.success("This ensures you have stable value when you need to withdraw, regardless of market conditions.")
            
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Apply this change", use_container_width=True, key="apply_cash"):
                    apply_portfolio_change(rec_stocks, rec_bonds)
                    st.success(f"Portfolio updated to {rec_stocks}% stocks, {rec_bonds}% bonds!")
                    st.balloons()
            with col2:
                if st.button("Go back", use_container_width=True, key="back_cash"):
                    st.session_state.page = 'scenarios'
                    del st.session_state.scenario
                    st.rerun()
        
        elif st.session_state.scenario == 'inflation':
            st.markdown("### Scenario: Inflation staying high")
            rec_stocks = 80
            rec_bonds = 20
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Current:** {current_stocks_pct}% Stocks, {current_bonds_pct}% Bonds")
            with col2:
                st.write(f"**Recommended:** {rec_stocks}% Stocks (with inflation protection), {rec_bonds}% Bonds")
            
            with st.expander("Why this recommendation?"):
                st.write(f"**Current Environment:** The Federal Reserve is raising interest rates (hence today's {market_context['sp500_change']:.1f}% drop) to fight inflation. Higher inflation erodes the purchasing power of your money over time.")
                st.write(f"**Your Current Holdings:** Tech stocks (Microsoft, Google, Tesla) don't protect well against inflation. They're down {market_context['tech_sector_change']:.1f}% today.")
                st.write(f"**Better Inflation Protection:** Consider shifting toward companies that can raise prices when costs go up. This includes: utility companies (everyone needs electricity), consumer staples (food, household goods), real estate funds, and commodity-related stocks (oil, materials).")
                st.write("**Trade-off:** More short-term volatility, but better long-term purchasing power protection.")
                st.write("**Cost:** Platform rebalancing fee: $12")
            
            st.info("Consider adding inflation-protected government bonds or commodity funds for even stronger inflation protection.")
            
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Apply this change", use_container_width=True, key="apply_inflation"):
                    apply_portfolio_change(rec_stocks, rec_bonds)
                    st.success(f"Portfolio updated to {rec_stocks}% stocks, {rec_bonds}% bonds!")
                    st.balloons()
            with col2:
                if st.button("Go back", use_container_width=True, key="back_inflation"):
                    st.session_state.page = 'scenarios'
                    del st.session_state.scenario
                    st.rerun()
        
        elif st.session_state.scenario == 'big_purchase':
            st.markdown("### Scenario: Saving for a big purchase")
            rec_stocks = 40
            rec_bonds = 60
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Current:** {current_stocks_pct}% Stocks, {current_bonds_pct}% Bonds")
            with col2:
                st.write(f"**Recommended:** {rec_stocks}% Stocks, {rec_bonds}% Bonds")
            
            with st.expander("Why this recommendation?"):
                st.write(f"**Today's Reality Check:** Your portfolio dropped ${abs(change_today):,} today. Imagine if your house closing or car purchase was TOMORROW - you'd have to sell at a loss.")
                st.write(f"**Volatility Risk:** With uncertainty high, expect more days like today. You can't afford that volatility near your purchase date.")
                st.write(f"**Bonds Provide Certainty:** Your bonds are up ${bonds_change:,} today while stocks dropped. Gradually shifting toward bonds as your purchase date approaches protects your funds.")
                st.write("**Trade-off:** Slower growth, but predictable value when you need to make your purchase.")
                st.write("**Cost:** Platform rebalancing fee: $12")
            
            st.success("This ensures you have the funds you need, regardless of whether markets are up or down on purchase day.")
            
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Apply this change", use_container_width=True, key="apply_purchase"):
                    apply_portfolio_change(rec_stocks, rec_bonds)
                    st.success(f"Portfolio updated to {rec_stocks}% stocks, {rec_bonds}% bonds!")
                    st.balloons()
            with col2:
                if st.button("Go back", use_container_width=True, key="back_purchase"):
                    st.session_state.page = 'scenarios'
                    del st.session_state.scenario
                    st.rerun()
        
        elif st.session_state.scenario == 'consistent':
            st.markdown("### Scenario: I need consistent returns")
            rec_stocks = 60
            rec_bonds = 40
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Current:** {current_stocks_pct}% Stocks, {current_bonds_pct}% Bonds")
            with col2:
                st.write(f"**Recommended:** {rec_stocks}% Dividend-paying Stocks, {rec_bonds}% Bonds")
            
            with st.expander("Why this recommendation?"):
                st.write(f"**Your Current Problem:** Tesla ({portfolio_holdings['Tesla']['percent']:.1f}% today) pays NO dividends. It's pure price volatility - you only make money if the stock price goes up.")
                st.write(f"**Market Context:** With uncertainty high, growth stocks like Tesla will continue to swing wildly up and down.")
                st.write("**What Would Change:** Replace high-volatility stocks with companies that pay you regular quarterly dividends regardless of stock price. Examples include utility companies (electricity, water), consumer staples (Procter & Gamble, Johnson & Johnson), and telecommunications companies.")
                st.write(f"**Real Numbers:** A 3-4% annual dividend yield means you earn ${int(total_stocks * 0.035):,}/year in cash deposits to your account, PLUS any stock price appreciation.")
                st.write("**Trade-off:** Lower growth ceiling than Tesla, but steady predictable income and less volatility.")
                st.write("**Cost:** Platform rebalancing fee: $12")
            
            st.info("Dividend-paying stocks provide regular income during market drops, which helps both emotionally (less stressful) and financially (cash flow).")
            
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Apply this change", use_container_width=True, key="apply_consistent"):
                    apply_portfolio_change(rec_stocks, rec_bonds)
                    st.success(f"Portfolio updated to {rec_stocks}% stocks, {rec_bonds}% bonds!")
                    st.balloons()
            with col2:
                if st.button("Go back", use_container_width=True, key="back_consistent"):
                    st.session_state.page = 'scenarios'
                    del st.session_state.scenario
                    st.rerun()
                    
        elif st.session_state.scenario == 'guide_me':
            st.markdown("### I'm not sure - Guide me")
            st.write("**No problem! Answer 3 quick questions and we'll recommend the right approach based on current market conditions.**")
            st.write("---")
            
            # Question 1
            if st.session_state.get('guide_step', 1) == 1:
                st.markdown("### Question 1 of 3: When do you need this money?")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Within 3 years", use_container_width=True):
                        st.session_state.guide_time = 'short'
                        st.session_state.guide_step = 2
                        st.rerun()
                with col2:
                    if st.button("3-10 years", use_container_width=True):
                        st.session_state.guide_time = 'medium'
                        st.session_state.guide_step = 2
                        st.rerun()
                with col3:
                    if st.button("10+ years", use_container_width=True):
                        st.session_state.guide_time = 'long'
                        st.session_state.guide_step = 2
                        st.rerun()
            
            # Question 2
            elif st.session_state.get('guide_step', 1) == 2:
                st.markdown("### Question 2 of 3: What are you saving for?")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Specific goal (house, car, education)", use_container_width=True):
                        st.session_state.guide_goal = 'specific'
                        st.session_state.guide_step = 3
                        st.rerun()
                with col2:
                    if st.button("Growing wealth / retirement", use_container_width=True):
                        st.session_state.guide_goal = 'wealth'
                        st.session_state.guide_step = 3
                        st.rerun()
                with col3:
                    if st.button("Emergency backup / safety net", use_container_width=True):
                        st.session_state.guide_goal = 'emergency'
                        st.session_state.guide_step = 3
                        st.rerun()
            
            # Question 3
            elif st.session_state.get('guide_step', 1) == 3:
                st.markdown("### Question 3 of 3: How much of your total savings is this?")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("A small portion (less than 25%)", use_container_width=True):
                        st.session_state.guide_capacity = 'small'
                        st.session_state.guide_step = 4
                        st.rerun()
                with col2:
                    if st.button("A significant chunk (25-75%)", use_container_width=True):
                        st.session_state.guide_capacity = 'significant'
                        st.session_state.guide_step = 4
                        st.rerun()
                with col3:
                    if st.button("Most/all my savings (75%+)", use_container_width=True):
                        st.session_state.guide_capacity = 'most'
                        st.session_state.guide_step = 4
                        st.rerun()
            
            # Recommendation
            elif st.session_state.get('guide_step', 1) == 4:
                st.markdown("### Here's our recommendation for you")
                
                time = st.session_state.get('guide_time', 'medium')
                goal = st.session_state.get('guide_goal', 'wealth')
                capacity = st.session_state.get('guide_capacity', 'significant')
                
                # Decision logic
                if capacity == 'most':
                    rec_stocks = 40
                    rec_bonds = 60
                    rationale = f"Since this represents most of your savings, we recommend a conservative approach. Given current market uncertainty, protecting your principal is critical."
                elif time == 'short':
                    rec_stocks = 30
                    rec_bonds = 70
                    rationale = f"With a short timeline and current market conditions (S&P {market_context['sp500_change']:.1f}% today), you can't risk a drop right before you need the money."
                elif time == 'long' and capacity == 'small' and goal == 'wealth':
                    rec_stocks = 80
                    rec_bonds = 20
                    rationale = f"You have time to ride out volatility, and this is a small portion of your savings. Even with today's {abs(market_context['sp500_change'])}% drop, long-term growth favors stocks."
                elif goal == 'emergency':
                    rec_stocks = 40
                    rec_bonds = 60
                    rationale = f"Emergency funds need stability. Your bonds are up ${bonds_change:,} today while stocks dropped - that's the stability you need."
                else:
                    rec_stocks = 60
                    rec_bonds = 40
                    rationale = f"Based on your timeline, goals, and current market volatility, a balanced approach works best."
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Current:** {current_stocks_pct}% Stocks, {current_bonds_pct}% Bonds")
                with col2:
                    st.write(f"**Recommended:** {rec_stocks}% Stocks, {rec_bonds}% Bonds")
                
                st.write("---")
                
                with st.expander("Why this recommendation?"):
                    st.write(f"**Why:** {rationale}")
                    st.write(f"**Your answers:** Timeline: {time}-term, Goal: {goal}, Portion: {capacity}")
                    st.write(f"**Market Context:** Uncertainty: {market_context['uncertainty_level']}, S&P 500: {market_context['sp500_change']:+.1f}%, Your portfolio today: ${change_today:,} ({percent_change:.1f}%)")
                    st.write("**Cost:** Platform rebalancing fee: $12")
                
                st.markdown("### What this means in practice")
                
                current_loss_20 = int(total_stocks * 0.20)
                rec_loss_20 = int(portfolio_value * (rec_stocks/100) * 0.20)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("If market drops 20%", f"Current: -${current_loss_20:,}")
                with col2:
                    st.metric("If market drops 20%", f"Recommended: -${rec_loss_20:,}")
                
                if rec_loss_20 < current_loss_20:
                    st.success(f"This reduces your potential loss by ${current_loss_20 - rec_loss_20:,}")
                
                st.info("You can always adjust this as market conditions or your situation changes.")
                
                st.write("---")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Apply this change", use_container_width=True, key="apply_guide"):
                        apply_portfolio_change(rec_stocks, rec_bonds)
                        st.success(f"Portfolio updated to {rec_stocks}% stocks, {rec_bonds}% bonds!")
                        st.balloons()
                with col2:
                    if st.button("Start over", use_container_width=True):
                        st.session_state.guide_step = 1
                        st.rerun()
    
    st.write("---")
    
    if st.button("Go back to home", use_container_width=True):
        st.session_state.page = 'home'
        if 'scenario' in st.session_state:
            del st.session_state.scenario
        if 'guide_step' in st.session_state:
            del st.session_state.guide_step
        st.rerun()