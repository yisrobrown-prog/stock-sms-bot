# 📈 Stock Price SMS Bot

Text any stock ticker to your Twilio phone number and instantly get the current price.

**Examples:**
- Text `AAPL` → "Apple Inc. (AAPL) 💵 USD 189.42 📈 +1.23 (+0.65%) today"
- Text `TSLA NVDA` → prices for both stocks
- Text `BTC-USD` → Bitcoin price

---

## 🚀 Setup (5 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a free Twilio account
1. Sign up at https://www.twilio.com (free trial includes a phone number)
2. From the Twilio Console, grab a phone number
3. Note your **Account SID** and **Auth Token** (you won't need them in the code — Twilio validates requests automatically via the webhook)

### 3. Expose your local server with ngrok
```bash
# Install ngrok from https://ngrok.com, then:
ngrok http 5000
```
Copy the `https://xxxx.ngrok.io` URL it gives you.

### 4. Configure your Twilio number
1. Go to **Twilio Console → Phone Numbers → Manage → Active Numbers**
2. Click your number
3. Under **Messaging → A message comes in**, set:
   - Webhook: `https://YOUR-NGROK-URL.ngrok.io/sms`
   - Method: `HTTP POST`
4. Save

### 5. Run the bot
```bash
python app.py
```

That's it! Text a ticker to your Twilio number. 🎉

---

## 📱 Usage

| You text | Bot replies |
|----------|-------------|
| `AAPL` | Apple price + daily change |
| `TSLA MSFT` | Both prices (up to 5 at once) |
| `BTC-USD` | Bitcoin in USD |
| `GOOGL` | Alphabet price |

---

## ☁️ Deploy to Production (optional)

To keep it running 24/7 without ngrok:

**Railway (free tier):**
```bash
# Install Railway CLI, then:
railway init
railway up
# Set the webhook URL to your Railway URL + /sms
```

**Heroku:**
```bash
echo "web: python app.py" > Procfile
heroku create
git push heroku main
```

**Render:** Connect your GitHub repo at https://render.com — free tier works great.

---

## 🔧 Customization

- **Multiple tickers at once:** Space or comma separated (up to 5)
- **Crypto:** Use Yahoo Finance symbols like `BTC-USD`, `ETH-USD`
- **International stocks:** `ASML`, `TSM`, `BABA`, etc.
