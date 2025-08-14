# Binance Testnet - Flask Trading Bot

Simple Flask app that runs a Binance **testnet** trading bot and shows a live Chart.js price chart with buy/sell markers.

---

## Features

* Runs a background trading bot using the `python-binance` client (testnet mode).
* Live web UI (Chart.js) showing price history and buy/sell markers.
* Start / Stop the bot from the UI.
* Manual **Buy Now** / **Sell Now** endpoints for demo/testing.
* Uses `.env` (or environment variables) for API keys — **no secrets committed**.
* Optional `force_initial_buy` to perform an immediate buy for demo purposes.

---

## Quickstart (local)

### 1. Clone repo

```bash
git clone https://github.com/Vaibhavsingh167/Binance_Testnet.git
cd Binance_Testnet
```

### 2. Create & activate a virtual environment

Linux / macOS:

```bash
python -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` should include:

```
Flask
python-binance
python-dotenv
```

### 4. Create `.env` (project root) — DO NOT COMMIT

Create a file named `.env` with:

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_SECRET_KEY=your_testnet_secret_here
```

Secure it locally:

```bash
chmod 600 .env
```

> Confirm `.env` is listed in `.gitignore` so it is not committed.

### 5. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser. The UI shows the current BTCUSDT price and a live chart. Use **Start Bot** and **Stop Bot** to control the trading bot.

---

## Configuration

All runtime config is in `bot.py` (you can edit to suit testing):

```python
symbol = 'BTCUSDT'
buy_price_threshold  = 118000
sell_price_threshold = 118800
trade_quantity       = 0.001
```

* `symbol` — Trading pair used on Binance testnet.
* `buy_price_threshold` — Bot buys when `price <= buy_price_threshold`.
* `sell_price_threshold` — Bot sells when `price >= sell_price_threshold`.
* `trade_quantity` — Quantity to trade per order (respect symbol min qty).

You can also start the bot with an immediate demo buy by passing `{"force_initial_buy": true}` in the `/start` POST body.

---

## API Endpoints

| Endpoint   | Method | Description                                                                 |
| ---------- | -----: | --------------------------------------------------------------------------- |
| `/`        |    GET | Web UI (chart + controls)                                                   |
| `/start`   |   POST | Start the bot. Accepts optional JSON body: `{ "force_initial_buy": true }`  |
| `/stop`    |   POST | Stop the bot                                                                |
| `/price`   |    GET | Returns `{ "price": <float> }` — latest price                               |
| `/history` |    GET | Returns `{"prices": [[time,price],...], "trades": [[time,price,side],...]}` |
| `/buy`     |   POST | Trigger manual buy (for demo)                                               |
| `/sell`    |   POST | Trigger manual sell (for demo)                                              |

Example `curl` to start with force buy:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"force_initial_buy": true}' \
     http://localhost:5000/start
```

Example manual buy:

```bash
curl -X POST http://localhost:5000/buy
```

---

## UI Notes

* The main chart uses Chart.js and the zoom/pan plugin.
* Blue line = price history. Green dots = buy trades. Red dots = sell trades.
* The UI polls `/price` and `/history` every 3 seconds for updates.
* You can zoom with the mouse wheel/pinch and pan horizontally (Ctrl + drag for pan, configured in UI).

---

## Testing & Demo Tips

* Use **Binance Testnet** API keys only when testing. Do **not** use real funds here.
* Set thresholds close to the current testnet price to see buys/sells quickly.
* Use `force_initial_buy` to preview sell behavior without waiting for a dip.
* If live orders fail due to minimum quantity or symbol restrictions on testnet, the bot still logs buy/sell markers using the latest price so the chart shows the activity.

---


* Never commit `.env` or real API keys to the repository.
* Use **testnet** keys for development and **never** run automatic real trading from CI.
* For production deployments, use your host platform’s secret store (e.g., GitHub Actions secrets, Heroku config vars, Railway/Render secrets) instead of `.env`.
* Rotate API keys immediately if they are ever leaked.

---

## Contributing

Contributions welcome. Please:

1. Fork the repo.
2. Create a feature branch `feature/my-feature`.
3. Open a PR with a clear summary of changes.

---

## License

This project is provided under the **MIT License** — see `LICENSE` (or add one) for details.

---

If you want, I can:

* paste the full final `README.md` contents to copy directly into your repo, OR
* generate and paste the `LICENSE` (MIT) text,
* create the GitHub Actions workflow file content and `Dockerfile` ready to add,
* or walk you step-by-step to commit and push these files to `https://github.com/Vaibhavsingh167/Binance_Testnet`.

