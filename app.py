import logging
import os
import sys
import time
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

import numpy as np
import ollama
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import timesfm
import torch
import yfinance as yf

OLLAMA_MODEL = "gemma4:e2b"
TIMESFM_REPO = "google/timesfm-2.5-200m-pytorch"
MAX_CONTEXT = 1024
MIN_HISTORY_LENGTH = 128
DEFAULT_HISTORY_LENGTH = 512
HISTORY_PERIOD = "max"


def suggested_history_days(horizon: int) -> int:
    if horizon <= 10:
        return 256
    if horizon <= 30:
        return 512
    return 1024
PLOTLY_CHART_CONFIG: dict[str, bool | list[str]] = {
    "scrollZoom": True,
    "displayModeBar": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [TimesFM] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
log = logging.getLogger("timesfm.app")

if os.getenv("HF_TOKEN"):
    log.info("HF_TOKEN loaded from .env (authenticated Hugging Face downloads)")
else:
    log.warning("HF_TOKEN not set — add it to .env for faster, more reliable downloads")


@st.cache_resource
def load_timesfm():
    log.info("load_timesfm: start")
    torch.set_float32_matmul_precision("high")
    log.info(
        "load_timesfm: downloading/loading %s (~1.8 GB on first run; watch this terminal)",
        TIMESFM_REPO,
    )
    t0 = time.time()
    model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(TIMESFM_REPO)
    log.info("load_timesfm: from_pretrained finished in %.1f s", time.time() - t0)

    log.info("load_timesfm: compiling forecast config")
    t1 = time.time()
    model.compile(timesfm.ForecastConfig(
        max_context=MAX_CONTEXT, max_horizon=256, normalize_inputs=True,
        use_continuous_quantile_head=True, force_flip_invariance=True,
        infer_is_positive=True, fix_quantile_crossing=True,
    ))
    log.info("load_timesfm: compile finished in %.1f s", time.time() - t1)
    log.info("load_timesfm: ready (total %.1f s)", time.time() - t0)
    return model


def forecast_stock(prices: np.ndarray, horizon: int) -> tuple[np.ndarray, np.ndarray]:
    prices_clean = np.array(prices, dtype=np.float32).flatten()
    log.info("forecast_stock: horizon=%d, input_len=%d", horizon, len(prices_clean))
    model = load_timesfm()
    t0 = time.time()
    point, quantiles = model.forecast(horizon=horizon, inputs=[prices_clean])
    log.info(
        "forecast_stock: done in %.1f s (device=cuda:%s)",
        time.time() - t0,
        torch.cuda.is_available(),
    )
    return point[0], quantiles[0]


def generate_market_report(
    ticker: str, last: float, mean: float, std: float,
    target: float, min_p: float, max_p: float,
) -> str:
    log.info("generate_market_report: calling Ollama model %s", OLLAMA_MODEL)
    prompt = (
        f"Perform financial analysis for {ticker}. Spot: ${last:.2f}, Mean: ${mean:.2f}, "
        f"Volatility: ${std:.2f}. TimesFM predicts 30-day target: ${target:.2f} "
        f"(Range: ${min_p:.2f} to ${max_p:.2f}). Write 4 short headers: "
        "1. Projections, 2. Support/Resistance, 3. Risk, 4. Outlook. "
        "No conversational filler or thinking tags."
    )
    res = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, options={"temperature": 0.0})
    return res["response"]


def build_chart(
    hist_df: pd.DataFrame,
    f_df: pd.DataFrame,
    actual_df: pd.DataFrame | None = None,
) -> go.Figure:
    traces: list[go.Scatter] = [
        go.Scatter(
            x=hist_df.index, y=hist_df["Close"],
            name="Historical", line=dict(color="#38bdf8"),
        ),
        go.Scatter(
            x=f_df.index, y=f_df["Point"],
            name="TimesFM Forecast", line=dict(color="#f43f5e", dash="dash"),
        ),
        go.Scatter(
            x=f_df.index, y=f_df["10th"], name="Support (10th)",
            line=dict(color="rgba(244,63,94,0.2)"), showlegend=False,
        ),
        go.Scatter(
            x=f_df.index, y=f_df["90th"], name="Resistance (90th)",
            fill="tonexty", fillcolor="rgba(244,63,94,0.08)",
            line=dict(color="rgba(244,63,94,0.2)"), showlegend=False,
        ),
    ]
    if actual_df is not None and not actual_df.empty:
        traces.append(go.Scatter(
            x=actual_df.index, y=actual_df["Close"],
            name="Actual (Backtest)", line=dict(color="#4ade80", width=2),
        ))
    fig = go.Figure(traces)
    fig.update_layout(
        template="plotly_dark",
        height=480,
        margin=dict(l=10, r=10, t=30, b=10),
        dragmode="zoom",
        hovermode="x unified",
        xaxis=dict(
            rangeslider=dict(visible=True, thickness=0.06),
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all", label="All"),
                ],
                bgcolor="rgba(30,41,59,0.9)",
                activecolor="#38bdf8",
            ),
            fixedrange=False,
        ),
        yaxis=dict(fixedrange=False),
    )
    return fig


@st.cache_data(show_spinner=False, ttl=300)
def download_prices(ticker: str) -> pd.DataFrame:
    """Download daily OHLCV history from Yahoo Finance with retries."""
    symbol = ticker.strip().upper()
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            df = yf.download(
                symbol,
                period=HISTORY_PERIOD,
                progress=False,
                threads=False,
                auto_adjust=True,
            )
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            if not df.empty:
                return df
            last_error = ValueError(f"No price data returned for {symbol}.")
        except Exception as exc:
            last_error = exc
        if attempt < 2:
            time.sleep(1 + attempt)
    raise ValueError(
        f"No price data returned for {symbol}. Check the ticker symbol."
    ) from last_error


def compute_backtest_metrics(
    predicted: np.ndarray, actual: np.ndarray,
) -> dict[str, float]:
    errors = predicted - actual
    pct_errors = errors / actual * 100
    return {
        "MAE": float(np.mean(np.abs(errors))),
        "RMSE": float(np.sqrt(np.mean(errors ** 2))),
        "MAPE": float(np.mean(np.abs(pct_errors))),
    }


def run_forecast(
    ticker: str,
    horizon: int,
    as_of_date: pd.Timestamp,
    history_length: int,
    price_df: pd.DataFrame | None = None,
) -> dict[str, object]:
    log.info(
        "run_forecast: ticker=%s horizon=%d as_of=%s history_length=%d",
        ticker, horizon, as_of_date.date(), history_length,
    )
    df = price_df if price_df is not None else download_prices(ticker)

    as_of_date = pd.Timestamp(as_of_date).normalize()
    latest_date = pd.Timestamp(df.index[-1]).normalize()
    if as_of_date > latest_date:
        raise ValueError(
            f"As-of date {as_of_date.date()} is after the latest available data "
            f"({latest_date.date()})."
        )

    hist_df = df.loc[df.index <= as_of_date].copy()
    if hist_df.empty:
        raise ValueError(f"No price data on or before {as_of_date.date()}.")

    total_history_days = len(hist_df)
    requested_history = min(history_length, MAX_CONTEXT)
    context_length = min(total_history_days, requested_history)
    history_insufficient = context_length < requested_history

    context_df = hist_df.tail(context_length)
    prices = context_df["Close"].values.flatten().astype(np.float32)
    log.info(
        "run_forecast: using %d context points ending %s",
        len(prices), context_df.index[-1].date(),
    )
    point, quantiles = forecast_stock(prices, horizon)

    as_of_ts = pd.Timestamp(context_df.index[-1])
    future_trading_days = df.index[df.index > as_of_ts][:horizon]
    if len(future_trading_days) >= horizon:
        dates = list(future_trading_days[:horizon])
    else:
        dates = [as_of_ts + timedelta(days=i) for i in range(1, horizon + 1)]

    f_df = pd.DataFrame({
        "Date": dates,
        "Point": point,
        "10th": quantiles[:, 1],
        "90th": quantiles[:, 9],
    }).set_index("Date")

    is_backtest = as_of_date < latest_date
    actual_df: pd.DataFrame | None = None
    metrics: dict[str, float] | None = None
    if is_backtest:
        actual_df = df.loc[df.index.isin(dates[:horizon]), ["Close"]].copy()
        if not actual_df.empty:
            compare_len = min(len(actual_df), len(point))
            metrics = compute_backtest_metrics(
                point[:compare_len],
                actual_df["Close"].values[:compare_len].astype(np.float64),
            )

    return {
        "ticker": ticker,
        "horizon": horizon,
        "requested_history_length": requested_history,
        "context_length": context_length,
        "total_history_days": total_history_days,
        "history_insufficient": history_insufficient,
        "as_of_date": as_of_ts,
        "is_backtest": is_backtest,
        "hist_df": hist_df,
        "f_df": f_df,
        "actual_df": actual_df,
        "metrics": metrics,
        "prices": prices,
    }


def render_forecasting_guide() -> None:
    with st.expander("📖 Forecasting guide", expanded=False):
        st.markdown(
            f"""
**History length** controls how many recent trading days TimesFM sees before predicting.
The model hard limit is **{MAX_CONTEXT:,}** days (~4 years).

#### Recommended history by forecast horizon

| Horizon | Suggested trading days | ~Calendar time |
|---------|------------------------|----------------|
| 10 days | **256** | ~1 year |
| 30 days | **512** | ~2 years |
| 60 days | **768–1024** | ~3–4 years |

**Rule of thumb:** use history about **8× to 20×** your forecast horizon.

- **Volatile assets** (e.g. `BTC-USD`) → lean toward **768–1024** days.
- **Stable large caps / ETFs** (e.g. `SPY`, `AAPL`) → **256–512** is often enough.

#### Trading days → calendar time

| Trading days | ~Years |
|--------------|--------|
| 126 | 6 months |
| 252 | 1 year |
| 512 | 2 years |
| 1024 | 4 years |

*(~252 trading days per year)*

#### Backtest metrics (when *Backtest As-of* > 0)

| MAPE | Typical read |
|------|----------------|
| &lt; 5% | Strong fit for this window |
| 5–10% | Moderate deviation |
| &gt; 10% | Forecast notably off actuals |

A single backtest on one ticker is a sanity check — run several dates and tickers
before drawing broad conclusions. Sharp crashes are especially hard for smoothing models.

#### Tickers

Any valid **Yahoo Finance** symbol works. See `ticker-catalog.md` in the repo for examples.
"""
        )


def main():
    st.set_page_config(page_title="TimesFM Stock Forecasting", layout="wide")
    st.title("📈 TimesFM Stock Forecasting & Reporting")
    render_forecasting_guide()

    ticker = st.sidebar.text_input("Stock Ticker", "BTC-USD").upper()
    horizon = st.sidebar.slider(
        "Forecast Horizon (Days)", 10, 60, 30,
        help="Number of future days to predict.",
    )
    suggested = suggested_history_days(horizon)
    history_length = st.sidebar.slider(
        "History Length (Trading Days)",
        MIN_HISTORY_LENGTH, MAX_CONTEXT, DEFAULT_HISTORY_LENGTH, step=128,
        help=(
            f"Recent trading days sent to TimesFM (max {MAX_CONTEXT:,}). "
            f"For a {horizon}-day horizon, ~{suggested} days is a good starting point."
        ),
    )
    if history_length != suggested:
        st.sidebar.caption(f"Suggested for {horizon}-day horizon: **{suggested}** days")
    else:
        st.sidebar.caption(f"Matches suggested **{suggested}** days for a {horizon}-day horizon")
    st.sidebar.caption(
        f"Only the most recent **{history_length:,}** days (up to **{MAX_CONTEXT:,}**) "
        f"are fed to the model."
    )
    days_back = st.sidebar.slider(
        "Backtest As-of (Trading Days Back)", 0, 120, 0,
        help="0 = latest available date (live forecast). "
             "Move back to cut the input series at a past date and compare against actual prices.",
    )
    run_clicked = st.sidebar.button("Run Forecasting Engine")

    if run_clicked:
        log.info("UI: Run Forecasting Engine clicked for %s", ticker)
        with st.status("Running forecast...", expanded=True) as status:
            try:
                status.write("Step 1/3 — Downloading price history...")
                probe = download_prices(ticker)
                latest = pd.Timestamp(probe.index[-1]).normalize()
                lookback_idx = max(0, len(probe.index) - 1 - days_back)
                as_of_date = pd.Timestamp(probe.index[lookback_idx]).normalize()
                status.write(
                    f"As-of date: **{as_of_date.date()}** "
                    f"({'backtest' if days_back > 0 else 'live forecast'}) — "
                    f"using **{history_length:,}** trading days of history."
                )
                status.write(
                    "Step 2/3 — Loading TimesFM model (~1.8 GB download on first run). "
                    "Watch the terminal running Streamlit for progress logs."
                )
                result = run_forecast(
                    ticker, horizon, as_of_date, history_length, price_df=probe,
                )
                status.write("Step 3/3 — Forecast complete.")
                status.update(label="Forecast complete", state="complete", expanded=False)
                st.session_state["forecast_result"] = result
                st.session_state.pop("report", None)
            except Exception as e:
                log.exception("Forecast failed")
                status.update(label="Forecast failed", state="error")
                st.error(f"Forecast failed: {e}")
                return

    result = st.session_state.get("forecast_result")
    if result is None:
        st.info(
            "Click **Run Forecasting Engine** to start.\n\n"
            "- **History length** (sidebar) sets how many recent trading days TimesFM sees.\n"
            "- **Backtest As-of** > 0 compares the forecast to actual prices and shows MAE/RMSE/MAPE.\n"
            "- **Text report** uses Ollama (optional — only needed after the chart appears).\n"
            "- No GPU → CPU inference is slower but works.\n\n"
            "Open **Forecasting guide** above for recommended history lengths by horizon.\n\n"
            "Tip: put `HF_TOKEN=...` in the `.env` file next to `app.py` for faster downloads."
        )
        return

    hist_df = result["hist_df"]
    f_df = result["f_df"]
    actual_df = result.get("actual_df")
    metrics = result.get("metrics")
    prices = result["prices"]
    result_ticker = str(result["ticker"])
    as_of_date = result["as_of_date"]

    context_note = (
        f"**{result['context_length']:,}** days sent to the model"
        f" (requested **{result['requested_history_length']:,}**,"
        f" **{result['total_history_days']:,}** available)"
    )
    if result.get("history_insufficient"):
        context_note += " — less history available than requested"

    if result.get("is_backtest"):
        st.caption(
            f"Backtest mode — forecasting from **{pd.Timestamp(as_of_date).date()}** "
            f"with {context_note}, **{result['horizon']}**-day horizon."
        )
        if metrics:
            m1, m2, m3 = st.columns(3)
            m1.metric("MAE", f"${metrics['MAE']:.2f}")
            m2.metric("RMSE", f"${metrics['RMSE']:.2f}")
            m3.metric("MAPE", f"{metrics['MAPE']:.2f}%")
        elif actual_df is not None and actual_df.empty:
            st.warning("No actual prices found in the forecast window for this as-of date.")
    else:
        st.caption(
            f"Live forecast from **{pd.Timestamp(as_of_date).date()}** with {context_note}."
        )

    st.plotly_chart(
        build_chart(hist_df, f_df, actual_df if result.get("is_backtest") else None),
        use_container_width=True,
        config=PLOTLY_CHART_CONFIG,
    )

    if "report" not in st.session_state:
        with st.spinner("Generating report (requires Ollama)..."):
            try:
                st.session_state["report"] = generate_market_report(
                    result_ticker,
                    float(prices[-1]),
                    float(np.mean(prices)),
                    float(np.std(prices)),
                    float(f_df["Point"].iloc[-1]),
                    float(f_df["10th"].min()),
                    float(f_df["90th"].max()),
                )
            except Exception as e:
                log.warning("Ollama report failed: %s", e)
                st.session_state["report"] = None
                st.warning(
                    f"Ollama report generation failed: {e}\n\n"
                    "Install Ollama from https://ollama.com, then run: `ollama pull gemma4:e2b`"
                )

    if st.session_state.get("report"):
        st.markdown(st.session_state["report"])


if __name__ == "__main__":
    main()
