import streamlit as st

st.set_page_config(page_title="Clarity Investments", layout="wide", initial_sidebar_state="collapsed")

# Professional UI styling
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #1a202c;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 0.75rem;
    }
    
    h4 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.75rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.15);
        width: 100%;
        letter-spacing: 0.01em;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a202c;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
        font-weight: 600;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .action-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .action-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        padding: 1rem 1.25rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 12px;
        font-weight: 600;
        padding: 1rem 1.25rem;
        font-size: 0.95rem;
        border: 1px solid #e2e8f0;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #edf2f7;
    }
    
    /* Text */
    p, .stMarkdown {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    /* Captions */
    .caption {
        color: #718096;
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e2e8f0;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom badge */
    .demo-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.375rem 0.875rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    
    /* Allocation display */
    .allocation-display {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #667eea30;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = 'loss'
if 'portfolio_allocation' not in st.session_state:
    st.session_state.portfolio_allocation = {'stocks': 70, 'bonds': 30}

# Market data
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

# Portfolio calculations
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

# ==========================================
# WELCOME SCREEN
# ==========================================
if st.session_state.page == 'welcome':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Welcome to Clarity Investments")
    st.write("Portfolio management made simple. We help everyday investors make confident decisions — whether you're just starting out or navigating market uncertainty.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("### I'm new here")
        st.write("Let's set up your first portfolio together. Takes 2 minutes.")
        st.write("")
        if st.button("Get Started", use_container_width=True, key="new_user"):
            st.session_state.page = 'onboarding'
            st.session_state.onboard_step = 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("### I already have a portfolio")
        st.write("Skip to your dashboard and see how your investments are doing.")
        st.write("")
        if st.button("Go to Dashboard", use_container_width=True, key="existing_user"):
            st.session_state.onboarded = True
            st.session_state.page = 'home'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# ONBOARDING
# ==========================================
elif st.session_state.page == 'onboarding':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Let's build your portfolio")
    st.write("Answer 3 quick questions. No finance jargon, we promise.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    
    if st.session_state.get('onboard_step', 1) == 1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Question 1 of 3: How much do you want to invest?")
        st.write("You can always add more later.")
        st.write("")
        amount = st.number_input("Investment Amount ($)", min_value=1000, max_value=1000000, value=50000, step=1000, label_visibility="collapsed")
        st.write("")
        if st.button("Next", use_container_width=True):
            st.session_state.investment_amount = amount
            st.session_state.onboard_step = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.get('onboard_step', 1) == 2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Question 2 of 3: When do you need this money?")
        st.write("This helps us balance growth vs. safety.")
        st.write("")
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            if st.button("Soon\n(less than 3 years)", use_container_width=True):
                st.session_state.onboard_timeline = 'short'
                st.session_state.onboard_step = 3
                st.rerun()
        with col2:
            if st.button("Medium term\n(3-10 years)", use_container_width=True):
                st.session_state.onboard_timeline = 'medium'
                st.session_state.onboard_step = 3
                st.rerun()
        with col3:
            if st.button("Long term\n(10+ years)", use_container_width=True):
                st.session_state.onboard_timeline = 'long'
                st.session_state.onboard_step = 3
                st.rerun()
        st.write("")
        if st.button("Back", use_container_width=True):
            st.session_state.onboard_step = 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.get('onboard_step', 1) == 3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Question 3 of 3: How would you feel if your investment dropped 15% in a month?")
        st.write("Be honest — there's no wrong answer.")
        st.write("")
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            if st.button("I'd panic\nand want to sell", use_container_width=True):
                st.session_state.onboard_comfort = 'low'
                st.session_state.onboard_step = 4
                st.rerun()
        with col2:
            if st.button("I'd be worried\nbut would hold", use_container_width=True):
                st.session_state.onboard_comfort = 'medium'
                st.session_state.onboard_step = 4
                st.rerun()
        with col3:
            if st.button("I'd be fine,\nmarkets recover", use_container_width=True):
                st.session_state.onboard_comfort = 'high'
                st.session_state.onboard_step = 4
                st.rerun()
        st.write("")
        if st.button("Back", use_container_width=True):
            st.session_state.onboard_step = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.get('onboard_step', 1) == 4:
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
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Your starting portfolio")
        st.write(f"Based on your answers, we recommend a **{description}** portfolio:")
        st.write("")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.metric("Stocks (Growth)", f"{stocks}%", f"${stocks_amount:,}")
            st.caption("Companies like Apple, Microsoft, index funds")
        with col2:
            st.metric("Bonds (Stability)", f"{bonds}%", f"${bonds_amount:,}")
            st.caption("Government and corporate bonds")
        
        st.write("")
        
        with st.expander("Why this mix?"):
            if stocks > 60:
                st.write(f"**Why more stocks:** You have a {timeline}-term timeline and feel comfortable with market swings. Stocks historically grow more over time.")
            elif bonds > 60:
                st.write(f"**Why more bonds:** With a {timeline}-term timeline, you need stability. Bonds are safer when you need money soon.")
            else:
                st.write("**Why balanced:** This gives you growth potential while protecting against big drops. It's a great starting point.")
            
            st.write("")
            
            potential_stock_loss = int(stocks_amount * 0.20)
            potential_bond_impact = int(bonds_amount * 0.01)
            net_loss = potential_stock_loss - potential_bond_impact
            
            potential_stock_gain = int(stocks_amount * 0.15)
            potential_bond_gain = int(bonds_amount * 0.02)
            net_gain = potential_stock_gain + potential_bond_gain
            
            st.write(f"**What this means:** If the stock market has a bad year (-20%), your stocks might lose ${potential_stock_loss:,}, but your bonds would likely stay steady or gain slightly (+${potential_bond_impact:,}). Net impact: around ${net_loss:,} loss.")
            st.write("")
            st.write(f"If the market has a great year (+15%), your stocks might gain ${potential_stock_gain:,}, plus bond gains (+${potential_bond_gain:,}). Net gain: around ${net_gain:,}.")
            st.write("")
            st.write("**You can adjust this anytime** as markets change or your life changes.")
        
        st.write("")
        st.success("Your portfolio is ready!")
        st.write("")
        
        if st.button("Go to Dashboard", use_container_width=True):
            st.session_state.onboarded = True
            st.session_state.portfolio_allocation = {'stocks': stocks, 'bonds': bonds}
            st.session_state.page = 'home'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# HOME SCREEN
# ==========================================
elif st.session_state.page == 'home':
    # Header with demo toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Clarity Investments")
    with col2:
        st.markdown(f'<span class="demo-badge">Demo: {st.session_state.demo_mode.title()} Mode</span>', unsafe_allow_html=True)
        st.write("")
        if st.button(f"Switch to {'Gain' if st.session_state.demo_mode == 'loss' else 'Loss'}"):
            st.session_state.demo_mode = 'gain' if st.session_state.demo_mode == 'loss' else 'loss'
            st.rerun()
    
    st.write("")
    
    # Portfolio value card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric(label="Your Portfolio", value=f"${portfolio_value:,}", delta=f"{change_today:,} ({percent_change:.1f}%)")
    st.write("")
    st.markdown(f'<div class="allocation-display"><strong>Current Allocation:</strong> {current_stocks_pct}% Stocks (${total_stocks:,}) | {current_bonds_pct}% Bonds (${total_bonds:,})</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    
    # Market context
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.caption(f"**Market News:** {market_context['news_headline']}")
    st.caption(f"**Market Context:** S&P 500 {market_context['sp500_change']:+.1f}% | Tech Sector {market_context['tech_sector_change']:+.1f}% | Uncertainty: {market_context['uncertainty_level']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    
    # Emotional messaging
    if change_today < 0:
        st.warning(f"Your portfolio dropped {abs(percent_change):.1f}% today, driven primarily by tech stock weakness (Microsoft {portfolio_holdings['Microsoft']['percent']:.1f}%, Tesla {portfolio_holdings['Tesla']['percent']:.1f}%). Markets typically recover within 18 months.")
    elif change_today > 0:
        st.success(f"Great news! Your portfolio gained ${abs(change_today):,} today")
    else:
        st.info("The market favors the disciplined. Stay on the path. Have a nice day.")
    
    st.write("")
    st.write("")
    
    # Action buttons
    st.markdown("### What would you like to do?")
    st.write("")
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("#### Take me to Safety")
        st.write("Reduce risk during market uncertainty")
        st.write("")
        if st.button("View Options", use_container_width=True, key="safety_btn"):
            st.session_state.page = 'safety'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("#### Show Actual Impact")
        st.write("See how each holding is performing")
        st.write("")
        if st.button("View Breakdown", use_container_width=True, key="impact_btn"):
            st.session_state.page = 'impact'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col3:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        st.markdown("#### What are my Options?")
        st.write("Explore scenarios and get recommendations")
        st.write("")
        if st.button("Explore Scenarios", use_container_width=True, key="scenarios_btn"):
            st.session_state.page = 'scenarios'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SAFETY PATH
# ==========================================
elif st.session_state.page == 'safety':
    st.title("Take me to Safety")
    st.write("")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("**We've created a safer version of your portfolio based on current market conditions.**")
    st.write("")
    
    safer_stocks = 50
    safer_bonds = 50
    amount_to_move = int((current_stocks_pct - safer_stocks) * portfolio_value / 100)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.write("**Current Portfolio**")
        st.write(f"**{current_stocks_pct}% Stocks** (${total_stocks:,})")
        st.write(f"**{current_bonds_pct}% Bonds** (${total_bonds:,})")
    with col2:
        st.write("**Recommended (Safer)**")
        st.write(f"**{safer_stocks}% Stocks** (${int(portfolio_value * safer_stocks / 100):,})")
        st.write(f"**{safer_bonds}% Bonds** (${int(portfolio_value * safer_bonds / 100):,})")
    
    st.write("")
    st.write("")
    
    st.markdown("### Quick Summary")
    if amount_to_move > 0:
        st.write(f"**Move ${amount_to_move:,} from stocks to bonds** to reduce risk in current volatile conditions.")
    
    st.write("")
    
    with st.expander("Why are we recommending this?"):
        st.write(f"**Market Analysis:** Current uncertainty is elevated. Tech stocks (which make up ${total_stocks - portfolio_holdings['S&P 500 Index Fund']['value']:,} of your portfolio) are down {market_context['tech_sector_change']:.1f}% today.")
        st.write("")
        st.write(f"**Your Holdings:** Microsoft lost ${abs(portfolio_holdings['Microsoft']['change']):,} today, Tesla lost ${abs(portfolio_holdings['Tesla']['change']):,}. Meanwhile, your bonds gained ${bonds_change:,}.")
        st.write("")
        st.write(f"**Why Bonds Now:** The Federal Reserve is raising interest rates to combat inflation. This typically hurts stocks in the short term but makes bonds more attractive. With bond interest rates at {market_context['bond_yield']}%, bonds are offering decent returns with much lower volatility.")
        st.write("")
        st.write(f"**Trade-off:** If the market rebounds quickly, you'll capture less upside. But given current conditions, stability matters more.")
        st.write("")
        st.write("**Cost:** Platform rebalancing fee: $12 per transaction")
    
    st.write("")
    st.write("")
    
    st.markdown("### What if the market drops another 20%?")
    st.write("")
    
    col1, col2 = st.columns(2, gap="large")
    current_loss = int(total_stocks * 0.20)
    safer_loss = int(portfolio_value * safer_stocks / 100 * 0.20)
    
    with col1:
        st.metric("Current Portfolio Impact", f"-${current_loss:,}", delta="-20% on stocks", delta_color="inverse")
    with col2:
        st.metric("Safer Portfolio Impact", f"-${safer_loss:,}", delta="-20% on stocks", delta_color="inverse")
    
    st.write("")
    st.success(f"The safer portfolio loses ${current_loss - safer_loss:,} less in a continued downturn.")
    st.info(f"This suggestion is based on current market uncertainty and your tech-heavy allocation.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("Apply this change", use_container_width=True):
            apply_portfolio_change(safer_stocks, safer_bonds)
            st.success("Portfolio updated! Your allocation is now 50% stocks, 50% bonds.")
            st.balloons()
    with col2:
        if st.button("Go back", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# Continue with Impact and Scenarios pages...
# (This file is getting long - the rest follows the same pattern with proper card styling)

# ==========================================
# IMPACT PATH
# ==========================================
elif st.session_state.page == 'impact':
    st.title("Show Actual Impact")
    st.write("")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Here's how your portfolio is performing today:")
    st.write("")
    st.markdown("**By Category:**")
    st.write("")
    
    stocks_percent_change = (stocks_change / total_stocks) * 100 if total_stocks > 0 else 0
    bonds_percent_change = (bonds_change / total_bonds) * 100 if total_bonds > 0 else 0
    
    with st.expander(f"Stocks: ${stocks_change:,} ({stocks_percent_change:+.1f}%) - Click to see details"):
        st.write("**Individual Stock Holdings:**")
        st.write("")
        for name, data in portfolio_holdings.items():
            if "Bond" not in name:
                st.write(f"• {name}: ${data['change']:,} ({data['percent']:+.1f}%)")
        st.write("")
        if st.session_state.demo_mode == 'loss':
            st.write(f"**Why the drop:** The tech sector is down {market_context['tech_sector_change']:.1f}% today. The Federal Reserve raised interest rates to slow inflation, which typically causes investors to sell growth stocks (like tech companies) in the short term and move to safer investments.")
        else:
            st.write(f"**Why the gain:** The tech sector is up today. Positive market sentiment and strong earnings reports are driving growth stocks higher.")
    
    with st.expander(f"Bonds: ${bonds_change:,} ({bonds_percent_change:+.1f}%) - Click to see details"):
        st.write("**Individual Bond Holdings:**")
        st.write("")
        for name, data in portfolio_holdings.items():
            if "Bond" in name:
                st.write(f"• {name}: ${data['change']:,} ({data['percent']:+.1f}%)")
        st.write("")
        if st.session_state.demo_mode == 'loss':
            st.write(f"**Why the gain:** When stock markets become uncertain, investors often move money into bonds for safety. Additionally, bond interest rates are at {market_context['bond_yield']}%, which is attractive compared to recent years.")
        else:
            st.write(f"**Why the modest gain:** Bonds provide steady returns through interest payments, even when stocks are doing well.")
    
    st.write("")
    
    if st.session_state.demo_mode == 'loss':
        st.info(f"**Summary:** Your tech stocks are down today due to a market-wide tech selloff (uncertainty is high), but bonds are holding steady as investors seek safety. This is normal during periods of market volatility.")
    else:
        st.info(f"**Summary:** Your tech stocks are performing well today, benefiting from positive market momentum. Your bonds continue to provide stable returns through interest payments.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("Go back to home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# ==========================================
# SCENARIOS PATH  
# ==========================================
elif st.session_state.page == 'scenarios':
    st.title("What are my options?")
    st.write("")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("**Tell us what you're thinking about, and we'll show you how to adjust your portfolio based on current market conditions.**")
    st.write("")
    
    st.markdown("### What are you worried about or planning for?")
    st.markdown("**Recommended if you're unsure:**")
    st.write("")
    if st.button("I'm not sure - Guide me through this", use_container_width=True, key="guide_highlighted"):
        st.session_state.scenario = 'guide_me'
        st.session_state.guide_step = 1
    
    st.write("")
    st.write("")
    st.markdown("**Or choose a specific scenario:**")
    st.write("")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("Market might crash", use_container_width=True):
            st.session_state.scenario = 'crash'
        st.write("")
        if st.button("I need cash in 1-2 years", use_container_width=True):
            st.session_state.scenario = 'cash_soon'
        st.write("")
        if st.button("Inflation staying high", use_container_width=True):
            st.session_state.scenario = 'inflation'
    with col2:
        if st.button("Saving for big purchase", use_container_width=True):
            st.session_state.scenario = 'big_purchase'
        st.write("")
        if st.button("I need consistent returns", use_container_width=True):
            st.session_state.scenario = 'consistent'
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    
    # Individual scenarios - I'll add one as example, you can replicate for others
    if 'scenario' in st.session_state and st.session_state.scenario == 'crash':
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Scenario: Market might crash")
        st.write("")
        
        rec_stocks = 50
        rec_bonds = 50
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.write(f"**Current:** {current_stocks_pct}% Stocks, {current_bonds_pct}% Bonds")
        with col2:
            st.write(f"**Recommended:** {rec_stocks}% Stocks, {rec_bonds}% Bonds")
        
        st.write("")
        
        with st.expander("Why this recommendation?"):
            st.write(f"**Current Market:** Uncertainty is elevated. S&P 500 is down {market_context['sp500_change']:.1f}% today. Tech sector (your largest exposure) is down {market_context['tech_sector_change']:.1f}%.")
            st.write("")
            st.write(f"**Your Portfolio:** Tesla is your most volatile holding ({portfolio_holdings['Tesla']['percent']:.1f}% today). Microsoft and Google are also down. Total tech exposure: ${total_stocks - portfolio_holdings['S&P 500 Index Fund']['value']:,}.")
            st.write("")
            st.write(f"**Why Move to Bonds:** Your bonds are UP today (+${bonds_change:,}) while stocks are down. This pattern (investors moving to safety) suggests more volatility ahead.")
            st.write("")
            st.write(f"**Trade-off:** If markets stabilize quickly, you'll miss some rebound gains.")
            st.write("")
            st.write("**Cost:** Platform rebalancing fee: $12")
        
        st.write("")
        crash_loss_current = int(total_stocks * 0.30)
        crash_loss_rec = int(portfolio_value * rec_stocks / 100 * 0.30)
        st.write(f"**If market drops 30%:** Current portfolio: -${crash_loss_current:,} | Recommended: -${crash_loss_rec:,}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")
        col1, col2 = st.columns(2, gap="large")
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
    
    # Add go back button at bottom
    st.write("")
    if st.button("Go back to home", use_container_width=True):
        st.session_state.page = 'home'
        if 'scenario' in st.session_state:
            del st.session_state.scenario
        if 'guide_step' in st.session_state:
            del st.session_state.guide_step
        st.rerun()
