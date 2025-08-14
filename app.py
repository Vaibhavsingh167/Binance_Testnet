from flask import Flask, render_template, jsonify, request
import bot

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    bot.start_bot()
    return jsonify({"status": "Bot started"})

@app.route("/stop", methods=["POST"])
def stop():
    bot.stop_bot()
    return jsonify({"status": "Bot stopped"})

@app.route("/price")
def price():
    try:
        price = bot.get_current_price()
        return jsonify({"price": price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/history")
def history():
    return jsonify({
        "prices": bot.price_history,
        "trades": bot.trade_history
    })

if __name__ == "__main__":
    app.run(debug=True)
