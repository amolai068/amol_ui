import streamlit as st
import pandas as pd
import random

def generate_stock_recommendations():
    stocks = ["RELIANCE", "HDFC", "TCS", "INFY", "ICICI", "BHARTIARTL", "HCLTECH"]
    prices = [random.uniform(1000, 3000) for _ in range(5)]
    targets = [price * random.uniform(1.05, 1.15) for price in prices]
    stop_losses = [price * random.uniform(0.92, 0.98) for price in prices]
    
    recommendations = pd.DataFrame({
        "Stock": random.sample(stocks, 5),
        "Entry Price": [round(p, 2) for p in prices],
        "Target": [round(t, 2) for t in targets],
        "Stop Loss": [round(sl, 2) for sl in stop_losses],
        "Expected Return": [f"{round((t/p-1)*100, 2)}%" for t, p in zip(targets, prices)]
    })


    return recommendations

def main():
    st.set_page_config(layout="wide", page_title="Trading Algorithm Platform")
    
    # Initialize session state variables if they don't exist
    if 'algo_started' not in st.session_state:
        st.session_state.algo_started = False
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'selected_trading_type' not in st.session_state:
        st.session_state.selected_trading_type = "Equity"
    if 'selected_strategy' not in st.session_state:
        st.session_state.selected_strategy = "1-strategy1-mid Short term trading (15 days cycle)"
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'algo_running' not in st.session_state:
        st.session_state.algo_running = False
    if 'positions' not in st.session_state:
        st.session_state.positions = pd.DataFrame(columns=['Stock', 'Quantity', 'Buy Price', 'Current Price', 'Target', 'Stop Loss', 'P&L', 'Status'])
    if 'holdings' not in st.session_state:
        st.session_state.holdings = []
    if 'tracking' not in st.session_state:
        st.session_state.tracking = False
    if 'sell_algo_running' not in st.session_state:
        st.session_state.sell_algo_running = False
    if 'option_algo_running' not in st.session_state:
        st.session_state.option_algo_running = False
    if 'commodity_algo_running' not in st.session_state:
        st.session_state.commodity_algo_running = False
    
    # Handle login first
    if not st.session_state.logged_in:
        st.title("Trading Algorithm Platform - Login")
        with st.container():
            st.subheader("Credentials")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input("Username", value="", key="username")
                # st.text_input("PAN", value="abd", key="pan")
            with col2:
                st.text_input("Password", type="password", value="", key="password")
            with col3:
                st.selectbox("Broker", 
                    ["Select Broker", "Zerodha", "Shoonya", "Fyers", "Flatrade", "Groww", "Upstox"],
                    key="broker"
                )
            
            if st.button("Login"):
                if st.session_state.broker != "Select Broker" and st.session_state.username and st.session_state.password:
                    st.session_state.logged_in = True
                    st.success(f"Successfully logged in to {st.session_state.broker}")
                    st.rerun()  # Updated to new rerun method
                else:
                    st.error("Please fill in all credentials")
        return  # Don't show anything else until logged in

    # Only show trading interface after successful login
    if st.session_state.logged_in:
        # Main trading interface in columns
        left_col, right_col= st.columns([1, 1])
        
        # Left column - Trading Types
        with left_col:
            st.subheader("Trading Types")
            trading_type = st.radio(
                "Select trading type:",
                ["Equity", "Options", "Commodity"],
                key="trading_type",
                horizontal=True
            )
            st.session_state.selected_trading_type = trading_type
            
            if trading_type == "Options":
                with st.container():
                    st.subheader("Options")
                    
                    # Add indices selection here
                    st.subheader("Select indices")
                    indices = st.multiselect(
                        "Choose indices:",
                        ["NIFTY", "BANKNIFTY", "FINNIFTY", "SENSEX", "MIDCAP","BAKEX"],
                        default=["NIFTY"],
                        key="indices"
                    )
                    
                    option_type = st.radio(
                        "Select option type:",
                        ["1-Directional", "2-non directional selling strategies", "3-Covered Call Strategies"],
                        key="option_type"
                    )
                
                    # Directional strategies section
                    if option_type == "1-Directional":
                        with st.container():
                            st.subheader("Directional strategies")
                            directional_strategy = st.selectbox(
                                "Select directional strategy:",
                                ["ML Trend Prediction", "Trend Follower", "Range Breakout","Custom strategy"],
                                key="directional_strategy"
                            )
                    
                    # Non-Directional strategies section
                    elif option_type == "2-non directional selling strategies":
                        with st.container():
                            st.subheader("Non Directional strategies")
                            non_directional_strategy = st.selectbox(
                                "Select non-directional strategy:",
                                ["custom strategy","Iron Condor", "Iron Butterfly", "Straddle", "Strangle", 
                                 "Calendar Spread", "Ratio Spread", "Butterfly Spread",
                                 "Box Spread", "Delta Neutral Trading", "Market Neutral Pairs Trading",
                                 "Gamma Scalping", "Volatility Arbitrage", "Dispersion Trading",
                                 "Statistical Arbitrage", "Convertible Arbitrage", "Risk Reversal",
                                 "Reverse Iron Condor", "Vega Neutral Trading", "Calendar Arbitrage",
                                 "Cash-and-Carry Arbitrage"],
                                key="non_directional_strategy"
                            )
                    
                    # Covered Call Strategies section
                    elif option_type == "3-Covered Call Strategies":
                        with st.container():
                            st.subheader("Covered Call Strategies")
                            covered_call_strategy = st.selectbox(
                                "Select covered call strategy:",
                                ["Strategy 1", "Strategy 2","Custom Strategy"],
                                key="covered_call_strategy"
                            )
                    
                    # Add Run and Stop Algo buttons for Options
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Run Options Algo"):
                            st.session_state.option_algo_running = True
                            st.success("Options Algo is running...")
                    with col2:
                        if st.button("Stop Options Algo"):
                            if st.session_state.option_algo_running:
                                st.session_state.option_algo_running = False
                                st.warning("Options Algo stopped!")
                            else:
                                st.info("Options Algo is not running")
            
            elif trading_type == "Commodity":
                with st.container():
                                        # Add MCX symbols selection
                    st.subheader("Select MCX Symbols")
                    mcx_symbols = [
                        "GOLD", "GOLDM", "GOLDGUINEA", "GOLDPETAL", "GOLDPETALDEL",
                        "SILVER", "SILVERM", "SILVERMIC", "SILVER1000",
                        "CRUDEOIL", "CRUDEOILM", "NATURALGAS", "NATURALGASM"
                    ]
                    selected_mcx_symbols = st.multiselect(
                        "Choose MCX symbols:",
                        mcx_symbols,
                        default=[],
                        key="mcx_symbols"
                    )






                    st.subheader("Commodity Strategies")
                    commodity_strategy = st.selectbox(
                        "Select commodity strategy:",
                        ["Strategy 1", "Strategy 2", "custom strategy1", "custom strategy2"],
                        key="commodity_strategy"
                    )
                    

                    
                    # Add Run and Stop Algo buttons for Commodity
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Run Commodity Algo"):
                            st.session_state.commodity_algo_running = True
                            st.success("Commodity Algo is running...")
                    with col2:
                        if st.button("Stop Commodity Algo"):
                            if st.session_state.commodity_algo_running:
                                st.session_state.commodity_algo_running = False
                                st.warning("Commodity Algo stopped!")
                            else:
                                st.info("Commodity Algo is not running")
            
            elif trading_type == "Equity":
                with st.container():
                    st.subheader("Equity Strategies")
                    equity_strategy = st.selectbox(
                        "Select equity strategy:",
                        ["NQ Strategy_1(Mid Short Term)", "NQ Strategy_2(Short Term)","Custom Strategy"],
                        key="equity_strategy"
                    )
                    
                    if st.button("Get Stock Recommendations"):
                        st.session_state.recommendations = generate_stock_recommendations()
                        st.session_state.algo_running = True
                        st.success("Generating stock recommendations...")

        # Right column - for displaying recommendations
        with right_col:
            if st.session_state.algo_running:
                if st.session_state.selected_trading_type == "Equity":
                    # 1. Recommendations Section
                    with st.expander("Stock Recommendations", expanded=True):
                        st.dataframe(st.session_state.recommendations[['Stock','Entry Price']], use_container_width=True)
                    
                    # 2. Order Placement Section
                    with st.expander("Place New Order", expanded=True):
                        st.subheader("Place Order")
                        selected_stock = st.selectbox(
                            "Select stock to buy:",
                            ["Select a stock..."] + st.session_state.recommendations['Stock'].tolist()
                        )
                        
                        if selected_stock != "Select a stock...":
                            col1, col2 = st.columns(2)
                            with col1:
                                quantity = st.number_input(
                                    "Enter Quantity:",
                                    min_value=1,
                                    value=1,
                                    key=f"qty_{selected_stock}"
                                )
                            with col2:
                                stock_price = st.session_state.recommendations[
                                    st.session_state.recommendations['Stock'] == selected_stock
                                ]['Entry Price'].iloc[0]
                                st.write(f"Total Amount: ₹{stock_price * quantity:,.2f}")
                            
                            if st.button("Place Buy Order", key="place_order"):
                                stock_data = st.session_state.recommendations[
                                    st.session_state.recommendations['Stock'] == selected_stock
                                ].iloc[0]
                                
                                new_position = pd.DataFrame({
                                    'Stock': [selected_stock],
                                    'Quantity': [quantity],
                                    'Buy Price': [stock_data['Entry Price']],
                                    'Current Price': [stock_data['Entry Price']],
                                    'Target': [stock_data['Target']],
                                    'Stop Loss': [stock_data['Stop Loss']],
                                    'P&L': [0],
                                    'Status': ['Active']
                                })
                                
                                st.session_state.positions = pd.concat(
                                    [st.session_state.positions, new_position],
                                    ignore_index=True
                                )
                                st.success(f"Order placed for {quantity} shares of {selected_stock}!")
                    
                    # 3. Portfolio Tracking Section
                    if not st.session_state.positions.empty:
                        with st.expander("Portfolio Tracker", expanded=True):
                            st.subheader("Active Positions")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("Track Portfolio", key="track_portfolio"):
                                    active_positions = st.session_state.positions[
                                        st.session_state.positions['Status'] == 'Active'
                                    ]
                                    
                                    if not active_positions.empty:
                                        for idx in active_positions.index:
                                            # Simulate price movement (replace with real price data)
                                            current_price = st.session_state.positions.loc[idx, 'Buy Price'] * (1 + random.uniform(-0.05, 0.05))
                                            st.session_state.positions.loc[idx, 'Current Price'] = round(current_price, 2)
                                            st.session_state.positions.loc[idx, 'P&L'] = round(
                                                (current_price - st.session_state.positions.loc[idx, 'Buy Price']) 
                                                * st.session_state.positions.loc[idx, 'Quantity'], 2
                                            )
                                            
                                            # Check for exit conditions
                                            if current_price >= st.session_state.positions.loc[idx, 'Target']:
                                                st.session_state.positions.loc[idx, 'Status'] = 'Exited (Target)'
                                                st.success(f"🎯 Target hit for {st.session_state.positions.loc[idx, 'Stock']}!")
                                            elif current_price <= st.session_state.positions.loc[idx, 'Stop Loss']:
                                                st.session_state.positions.loc[idx, 'Status'] = 'Exited (Stop Loss)'
                                                st.warning(f"⚠️ Stop loss hit for {st.session_state.positions.loc[idx, 'Stock']}!")

                            with col2:
                                if st.button("Start Portfolio Stock Sell Algo"):
                                    st.session_state.sell_algo_running = True
                                    st.success("Portfolio Stock Sell Algo started!")

                            with col3:
                                if st.button("Stop Portfolio Stock Sell Algo"):
                                    if st.session_state.sell_algo_running:
                                        st.session_state.sell_algo_running = False
                                        st.warning("Portfolio Stock Sell Algo stopped!")
                                    else:
                                        st.info("Sell Algo is not running")
                            
                            if st.session_state.sell_algo_running:
                                st.info("Sell Algo is actively monitoring positions for optimal exit points")
                            
                            st.dataframe(st.session_state.positions, use_container_width=True)
                            total_pnl = st.session_state.positions['P&L'].sum()
                            st.metric("Total P&L", f"₹{total_pnl:,.2f}", delta=total_pnl)
                else:
                    st.info("Run the algorithm to get recommendations")

if __name__ == "__main__":
    main()
