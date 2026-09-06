import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def get_gold_prices():
    url = "https://data-asg.goldprice.org/dbXRates/SAR"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    item = data["items"][0]

    ounce_price = float(item["xauPrice"])

    gram_24 = ounce_price / 31.1034768
    gram_22 = gram_24 * 22 / 24
    gram_21 = gram_24 * 21 / 24
    gram_18 = gram_24 * 18 / 24

    return gram_24, gram_22, gram_21, gram_18


def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
        },
        timeout=20,
    )

    response.raise_for_status()


def main():
    prices = get_gold_prices()
    g24, g22, g21, g18 = prices

    now = datetime.now(ZoneInfo("Asia/Riyadh"))
    updated = now.strftime("%Y-%m-%d %H:%M")

    message = f"""🇸🇦 <b>أسعار الذهب في السعودية</b> 🥇

🔸 <b>عيار 24:</b> {g24:.2f} ريال/غرام
🔸 <b>عيار 22:</b> {g22:.2f} ريال/غرام
🔸 <b>عيار 21:</b> {g21:.2f} ريال/غرام
🔸 <b>عيار 18:</b> {g18:.2f} ريال/غرام

🕐 <b>آخر تحديث:</b> {updated}
📍 السعر تقريبي ولا يشمل المصنعية والضريبة.

@GoldSaudiB
"""

    send_message(message)
    print("تم إرسال أسعار الذهب إلى القناة بنجاح ✅")


if __name__ == "__main__":
    main()
