# Ticker Catalog

The dashboard accepts **any valid Yahoo Finance symbol** in the sidebar (`Stock Ticker`). Data is fetched via `yfinance`; if `yf.download(ticker)` returns rows, the forecast can run.

Symbols are **case-insensitive** (the app uppercases input). Use the exact Yahoo Finance format below.

> **Note:** Yahoo Finance has tens of thousands of symbols. This catalog lists commonly used tickers grouped by asset class. Symbols not listed here may still work if they exist on Yahoo Finance.

---

## US Equities — Mega-cap & popular


| Ticker  | Name                                      |
| ------- | ----------------------------------------- |
| `AAPL`  | Apple                                     |
| `MSFT`  | Microsoft                                 |
| `GOOGL` | Alphabet (Class A)                        |
| `GOOG`  | Alphabet (Class C)                        |
| `AMZN`  | Amazon                                    |
| `META`  | Meta Platforms                            |
| `NVDA`  | NVIDIA                                    |
| `TSLA`  | Tesla                                     |
| `BRK-B` | Berkshire Hathaway (Class B)              |
| `JPM`   | JPMorgan Chase                            |
| `V`     | Visa                                      |
| `MA`    | Mastercard                                |
| `UNH`   | UnitedHealth                              |
| `XOM`   | Exxon Mobil                               |
| `JNJ`   | Johnson & Johnson                         |
| `WMT`   | Walmart                                   |
| `PG`    | Procter & Gamble                          |
| `HD`    | Home Depot                                |
| `BAC`   | Bank of America                           |
| `KO`    | Coca-Cola                                 |
| `PEP`   | PepsiCo                                   |
| `DIS`   | Walt Disney                               |
| `NFLX`  | Netflix                                   |
| `AMD`   | Advanced Micro Devices                    |
| `INTC`  | Intel                                     |
| `CRM`   | Salesforce                                |
| `ORCL`  | Oracle                                    |
| `COST`  | Costco                                    |
| `ABBV`  | AbbVie                                    |
| `LLY`   | Eli Lilly                                 |
| `AVGO`  | Broadcom                                  |
| `MRK`   | Merck                                     |
| `TMO`   | Thermo Fisher                             |
| `ADBE`  | Adobe                                     |
| `CSCO`  | Cisco                                     |
| `ACN`   | Accenture                                 |
| `NKE`   | Nike                                      |
| `MCD`   | McDonald's                                |
| `BA`    | Boeing                                    |
| `GS`    | Goldman Sachs                             |
| `MS`    | Morgan Stanley                            |
| `UBER`  | Uber                                      |
| `ABNB`  | Airbnb                                    |
| `COIN`  | Coinbase                                  |
| `PLTR`  | Palantir                                  |
| `SOFI`  | SoFi                                      |
| `RIVN`  | Rivian                                    |
| `LCID`  | Lucid                                     |
| `GME`   | GameStop                                  |
| `AMC`   | AMC Entertainment                         |
| `SPY`   | SPDR S&P 500 ETF (also listed under ETFs) |


---

## US ETFs — Broad market & sectors


| Ticker | Name                                    |
| ------ | --------------------------------------- |
| `SPY`  | SPDR S&P 500                            |
| `QQQ`  | Invesco QQQ (Nasdaq-100)                |
| `IWM`  | iShares Russell 2000                    |
| `DIA`  | SPDR Dow Jones Industrial Average       |
| `VTI`  | Vanguard Total Stock Market             |
| `VOO`  | Vanguard S&P 500                        |
| `IVV`  | iShares Core S&P 500                    |
| `VEA`  | Vanguard FTSE Developed Markets         |
| `VWO`  | Vanguard FTSE Emerging Markets          |
| `EFA`  | iShares MSCI EAFE                       |
| `EEM`  | iShares MSCI Emerging Markets           |
| `XLK`  | Technology Select Sector                |
| `XLF`  | Financial Select Sector                 |
| `XLE`  | Energy Select Sector                    |
| `XLV`  | Health Care Select Sector               |
| `XLI`  | Industrial Select Sector                |
| `XLY`  | Consumer Discretionary Select Sector    |
| `XLP`  | Consumer Staples Select Sector          |
| `XLU`  | Utilities Select Sector                 |
| `XLB`  | Materials Select Sector                 |
| `XLRE` | Real Estate Select Sector               |
| `XLC`  | Communication Services Select Sector    |
| `ARKK` | ARK Innovation                          |
| `SOXX` | iShares Semiconductor                   |
| `SMH`  | VanEck Semiconductor                    |
| `GLD`  | SPDR Gold Shares                        |
| `SLV`  | iShares Silver Trust                    |
| `USO`  | United States Oil Fund                  |
| `TLT`  | iShares 20+ Year Treasury Bond          |
| `IEF`  | iShares 7–10 Year Treasury Bond         |
| `SHY`  | iShares 1–3 Year Treasury Bond          |
| `HYG`  | iShares High Yield Corporate Bond       |
| `LQD`  | iShares Investment Grade Corporate Bond |
| `VNQ`  | Vanguard Real Estate                    |
| `BITO` | ProShares Bitcoin Strategy ETF          |


---

## Market indices


| Ticker      | Name                         |
| ----------- | ---------------------------- |
| `^GSPC`     | S&P 500 Index                |
| `^DJI`      | Dow Jones Industrial Average |
| `^IXIC`     | Nasdaq Composite             |
| `^NDX`      | Nasdaq-100 Index             |
| `^RUT`      | Russell 2000                 |
| `^VIX`      | CBOE Volatility Index        |
| `^FTSE`     | FTSE 100                     |
| `^GDAXI`    | DAX (Germany)                |
| `^FCHI`     | CAC 40 (France)              |
| `^N225`     | Nikkei 225 (Japan)           |
| `^HSI`      | Hang Seng (Hong Kong)        |
| `^STOXX50E` | Euro Stoxx 50                |


---

## Cryptocurrency (USD pairs)


| Ticker      | Name              |
| ----------- | ----------------- |
| `BTC-USD`   | Bitcoin           |
| `ETH-USD`   | Ethereum          |
| `BNB-USD`   | BNB               |
| `SOL-USD`   | Solana            |
| `XRP-USD`   | XRP               |
| `ADA-USD`   | Cardano           |
| `DOGE-USD`  | Dogecoin          |
| `AVAX-USD`  | Avalanche         |
| `DOT-USD`   | Polkadot          |
| `MATIC-USD` | Polygon (POL)     |
| `LINK-USD`  | Chainlink         |
| `LTC-USD`   | Litecoin          |
| `BCH-USD`   | Bitcoin Cash      |
| `UNI-USD`   | Uniswap           |
| `ATOM-USD`  | Cosmos            |
| `XLM-USD`   | Stellar           |
| `ETC-USD`   | Ethereum Classic  |
| `FIL-USD`   | Filecoin          |
| `APT-USD`   | Aptos             |
| `ARB-USD`   | Arbitrum          |
| `OP-USD`    | Optimism          |
| `NEAR-USD`  | NEAR Protocol     |
| `ICP-USD`   | Internet Computer |
| `HBAR-USD`  | Hedera            |
| `VET-USD`   | VeChain           |
| `ALGO-USD`  | Algorand          |
| `SHIB-USD`  | Shiba Inu         |


---

## Forex (Yahoo format: `PAIR=X`)


| Ticker     | Pair                           |
| ---------- | ------------------------------ |
| `EURUSD=X` | Euro / US Dollar               |
| `GBPUSD=X` | British Pound / US Dollar      |
| `USDJPY=X` | US Dollar / Japanese Yen       |
| `USDCHF=X` | US Dollar / Swiss Franc        |
| `AUDUSD=X` | Australian Dollar / US Dollar  |
| `USDCAD=X` | US Dollar / Canadian Dollar    |
| `NZDUSD=X` | New Zealand Dollar / US Dollar |
| `EURGBP=X` | Euro / British Pound           |
| `EURJPY=X` | Euro / Japanese Yen            |
| `GBPJPY=X` | British Pound / Japanese Yen   |


---

## Commodities & futures (`=F` suffix)


| Ticker | Name                    |     |
| ------ | ----------------------- | --- |
| `GC=F` | Gold futures            |     |
| `SI=F` | Silver futures          |     |
| `CL=F` | Crude oil (WTI) futures |     |
| `BZ=F` | Brent crude futures     |     |
| `NG=F` | Natural gas futures     |     |
| `HG=F` | Copper futures          |     |
| `PL=F` | Platinum futures        |     |
| `PA=F` | Palladium futures       |     |
| `ZC=F` | Corn futures            |     |
| `ZS=F` | Soybean futures         |     |
| `ZW=F` | Wheat futures           |     |


---

## International equities (Yahoo suffix examples)


| Ticker        | Market / Name                   |
| ------------- | ------------------------------- |
| `TSM`         | Taiwan Semiconductor (US ADR)   |
| `BABA`        | Alibaba (US ADR)                |
| `NIO`         | NIO (US ADR)                    |
| `SONY`        | Sony (US ADR)                   |
| `SAP`         | SAP (US ADR)                    |
| `BP`          | BP (US ADR)                     |
| `SHEL`        | Shell (US listing)              |
| `ASML`        | ASML (US listing)               |
| `SHOP`        | Shopify                         |
| `RY.TO`       | Royal Bank of Canada (Toronto)  |
| `TD.TO`       | Toronto-Dominion Bank           |
| `BHP.AX`      | BHP Group (Australia)           |
| `CBA.AX`      | Commonwealth Bank (Australia)   |
| `7203.T`      | Toyota (Tokyo)                  |
| `9984.T`      | SoftBank Group (Tokyo)          |
| `0700.HK`     | Tencent (Hong Kong)             |
| `9988.HK`     | Alibaba (Hong Kong)             |
| `RELIANCE.NS` | Reliance Industries (NSE India) |
| `TCS.NS`      | Tata Consultancy (NSE India)    |
| `INFY.NS`     | Infosys (NSE India)             |


**Common exchange suffixes on Yahoo Finance:**


| Suffix       | Exchange                    |
| ------------ | --------------------------- |
| `.TO`        | Toronto                     |
| `.L`         | London                      |
| `.PA`        | Paris                       |
| `.DE` / `.F` | Germany (XETRA / Frankfurt) |
| `.AX`        | Australia                   |
| `.HK`        | Hong Kong                   |
| `.T`         | Tokyo                       |
| `.NS`        | NSE India                   |
| `.BO`        | BSE India                   |
| `.SW`        | Switzerland                 |
| `.SA`        | São Paulo                   |


---

## How to verify a ticker

In Python:

```python
import yfinance as yf
df = yf.download("BTC-USD", period="5d", progress=False)
print(df.empty)  # False = ticker works
```

Or enter the symbol in the Streamlit sidebar and click **Run Forecasting Engine**. If Yahoo returns no data, the app shows: `No price data returned for {ticker}`.

---

## Default in the app

The sidebar default is `**BTC-USD`**.