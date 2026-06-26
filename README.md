<div align="center">
  <a href="https://youtu.be/t4jkgyfbE68">
    <img src="https://img.youtube.com/vi/t4jkgyfbE68/0.jpg" alt="Google's New TimesFM 2.5 Just Changed AI Stock Forecasting Forever!">
  </a>
  <h3>📺 <a href="https://youtu.be/t4jkgyfbE68">Watch the full tutorial on YouTube</a></h3>
</div>

# Google's New TimesFM 2.5 Just Changed AI Stock Forecasting Forever!

A premium, high-performance time-series forecasting and automated market analysis system. This repository integrates **Google's TimesFM 2.5** (Time Series Foundation Model) for advanced predictive analysis with **Ollama** (`gemma4:e2b`) for generating comprehensive, automated market reports.

---

## 🛠️ Tech Stack

- **Time-Series forecasting**: `TimesFM 2.5` (`google/timesfm-2.5-200m-pytorch`)
- **Automated Market Reporting**: `Ollama` (`gemma4:e2b`)
- **Dashboard Interface**: `Streamlit` with a customized glassmorphic dark-theme UI
- **Data Acquisition**: `yfinance` (Yahoo Finance API)
- **Visualizations**: `Plotly` (Interactive charts with confidence bands)
- **Scientific Computing**: `PyTorch`, `NumPy`, `Pandas`

---

## 📂 File Directory Structure

- 💾 `app.py` — The interactive Streamlit dashboard combining data loading, TimesFM forecasting, and Ollama reporting in under 75 lines of code.
- 📊 `report_snapshot.md` — Pre-generated analysis output matching the dashboard output layout for zero-latency initial view.
- 📋 `requirements.txt` — Project dependencies list.

---

## ⚙️ Installation

Open your Windows PowerShell terminal and run the following commands sequentially:

```powershell
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
.venv\Scripts\Activate.ps1

# 3. Install core dependencies
pip install -r requirements.txt
```

> [!NOTE]
> This repository contains the application and dashboard code. If you would like to explore or contribute to the core TimesFM model itself, please clone the official Google Research repository:
> ```bash
> git clone https://github.com/google-research/timesfm.git
> ```

---

## 🚀 How to Run the Dashboard

To start the interactive Streamlit dashboard, run this command in your active PowerShell window:

```powershell
streamlit run app.py
```

---

## 🔮 Use Cases

1. **Long-Term Asset Allocation**: Forecast asset price ranges over 30 to 90 days to determine risk-adjusted weighting.
2. **Support & Resistance Discovery**: Use TimesFM quantile boundaries (10th/90th percentile) to identify statistical support and resistance bands.
3. **Portfolio Stress-Testing**: Generate downside scenario estimates from the 10th percentile quantile path.
4. **Automated Investment Memorandums**: Produce markdown-formatted analyst notes combining quantitative TimesFM predictions with LLM synthesis.
5. **Earnings Announcement Risk Assessment**: Forecast pre-earnings volatility paths to plan options and hedging strategies.

---

## 🗺️ Future Roadmap

1. **Exogenous Covariates (XReg)**: Integrate macroeconomic indices and sector-specific indicators.
2. **Multi-Asset Portfolio Optimization**: Allow simultaneous forecasting across multiple correlated tickers.
3. **Real-time News Sentiment Bias**: Adjust forecast paths based on live financial sentiment scores.
4. **Custom LoRA Fine-Tuning**: Enable users to fine-tune TimesFM checkpoints on custom proprietary transactional data.
5. **Backtesting Framework**: Include automated backtesting metrics (MAPE, MSE) over historical validation windows.

---

## Keywords

`TimesFM 2.5` `Google AI` `Time-Series Forecasting` `Stock Market Prediction` `Ollama` `Gemma 2` `Streamlit` `yfinance` `Quantitative Finance` `Machine Learning` `Financial Analysis` `AI Stock Forecasting`
