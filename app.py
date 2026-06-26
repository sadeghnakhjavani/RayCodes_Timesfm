import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import ollama
import timesfm
import torch
from datetime import datetime, timedelta

OLLAMA_MODEL = "gemma4:e2b"

@st.cache_resource
def load_timesfm():
    torch.set_float32_matmul_precision("high")
    model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
    model.compile(timesfm.ForecastConfig(
        max_context=1024, max_horizon=256, normalize_inputs=True,
        use_continuous_quantile_head=True, force_flip_invariance=True,
        infer_is_positive=True, fix_quantile_crossing=True
    ))
    return model

def forecast_stock(prices: np.ndarray, horizon: int) -> tuple[np.ndarray, np.ndarray]:
    prices_clean = np.array(prices, dtype=np.float32).flatten()
    model = load_timesfm()
    point, quantiles = model.forecast(horizon=horizon, inputs=[prices_clean])
    return point[0], quantiles[0]

def generate_market_report(ticker: str, last: float, mean: float, std: float, target: float, min_p: float, max_p: float) -> str:
    prompt = f"Perform financial analysis for {ticker}. Spot: ${last:.2f}, Mean: ${mean:.2f}, Volatility: ${std:.2f}. TimesFM predicts 30-day target: ${target:.2f} (Range: ${min_p:.2f} to ${max_p:.2f}). Write 4 short headers: 1. Projections, 2. Support/Resistance, 3. Risk, 4. Outlook. No conversational filler or thinking tags."
    res = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, options={"temperature": 0.0})
    return res["response"]

def main():
    st.set_page_config(page_title="TimesFM Stock Forecasting", layout="wide")
    st.title("📈 TimesFM Stock Forecasting & Reporting")
    
    ticker = st.sidebar.text_input("Stock Ticker", "MSFT").upper()
    horizon = st.sidebar.slider("Forecast Horizon (Days)", 10, 60, 30)
    
    if st.sidebar.button("Run Forecasting Engine") or "snapshot" in st.session_state:
        st.session_state["snapshot"] = True
        
        df = yf.download(ticker, period="6mo")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        prices = df["Close"].values.flatten().astype(np.float32)
        point, quantiles = forecast_stock(prices, horizon)
        
        dates = [df.index[-1] + timedelta(days=i) for i in range(1, horizon + 1)]
        f_df = pd.DataFrame({"Date": dates, "Point": point, "10th": quantiles[:, 1], "90th": quantiles[:, 9]}).set_index("Date")
        
        fig = go.Figure([
            go.Scatter(x=df.index, y=df["Close"], name="Historical", line=dict(color="#38bdf8")),
            go.Scatter(x=f_df.index, y=f_df["Point"], name="TimesFM Forecast", line=dict(color="#f43f5e", dash="dash")),
            go.Scatter(x=f_df.index, y=f_df["10th"], name="Support (10th)", line=dict(color="rgba(244,63,94,0.2)"), showlegend=False),
            go.Scatter(x=f_df.index, y=f_df["90th"], name="Resistance (90th)", fill="tonexty", fillcolor="rgba(244,63,94,0.08)", line=dict(color="rgba(244,63,94,0.2)"), showlegend=False)
        ])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
        with st.spinner("Generating Report..."):
            try:
                report = generate_market_report(ticker, float(prices[-1]), float(np.mean(prices)), float(np.std(prices)), float(f_df["Point"].iloc[-1]), float(f_df["10th"].min()), float(f_df["90th"].max()))
                st.markdown(report)
            except Exception as e:
                st.warning(f"Ollama generation failed: {e}")
    else:
        pass

if __name__ == "__main__":
    main()
