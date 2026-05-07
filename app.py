"""
Stock Price SMS Bot
Text a stock ticker to your Twilio number → get back the current price.
"""

from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import yfinance as yf

app = Flask(__name__)


def get_stock_price(ticker: str) -> str:
    """Fetch current stock price using yfinance."""
    try:
        ticker = ticker.upper().strip()
        stock = yf.Ticker(ticker)
        info = stock.info

        # Try fast_info first (more reliable for current price)
        fast = stock.fast_info
        price = getattr(fast, "last_price", None)

        if price is None:
            price = info.get("currentPrice") or info.get("regularMarketPrice")

        if price is None:
            return f'❌ Could not find price for "{ticker}". Check the ticker and try again.'

        name = info.get("shortName") or info.get("longName") or ticker
        currency = info.get("currency", "USD")

        # Get change info
        prev_close = getattr(fast, "previous_close", None) or info.get("previousClose")
        if prev_close and prev_close > 0:
            change = price - prev_close
            pct = (change / prev_close) * 100
            arrow = "📈" if change >= 0 else "📉"
            sign = "+" if change >= 0 else ""
            change_str = f"\n{arrow} {sign}{change:.2f} ({sign}{pct:.2f}%) today"
        else:
            change_str = ""

        return (
            f"📊 {name} ({ticker})\n"
            f"💵 {currency} {price:,.2f}"
            f"{change_str}"
        )

    except Exception as e:
        return f'⚠️ Error looking up "{ticker}": {str(e)}'


@app.route("/sms", methods=["POST"])
def sms_reply():
    """Handle incoming SMS from Twilio."""
    body = request.form.get("Body", "").strip()
    resp = MessagingResponse()

    if not body:
        resp.message("Please text a stock ticker symbol (e.g. AAPL, TSLA, MSFT).")
        return Response(str(resp), mimetype="text/xml")

    # Support multiple tickers separated by spaces or commas
    tickers = [t.strip() for t in body.replace(",", " ").split() if t.strip()]

    if len(tickers) > 5:
        resp.message("⚠️ Please send up to 5 tickers at a time.")
        return Response(str(resp), mimetype="text/xml")

    results = [get_stock_price(t) for t in tickers]
    reply = "\n\n".join(results)

    resp.message(reply)
    return Response(str(resp), mimetype="text/xml")


@app.route("/", methods=["GET"])
def index():
    return "📈 Stock SMS Bot is running! Configure your Twilio webhook to /sms"


if __name__ == "__main__":
    print("🚀 Stock SMS Bot starting on http://localhost:5000")
    print("   Webhook endpoint: http://localhost:5000/sms")
    app.run(debug=True, port=5000)
