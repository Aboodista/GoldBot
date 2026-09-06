import os
from datetime import datetime
import requests
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def get_gold_prices():
    # استخدمنا رابط مباشر لبيانات الذهب
    url = "https://data-asg.goldprice.org/dbXRates/USD"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://goldprice.org/",
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    data = response.json()
    item = data["items"][0]

    # السعر بالدولار للأونصة
    # تحويله إلى الريال السعودي (1 دولار = 3.75 ريال)
    ounce_price_usd = float(item["xauPrice"])
    ounce_price_sar = ounce_price_usd * 3.75

    # تحويل سعر الأونصة إلى سعر الغرام
    gram_24 = ounce_price_sar / 31.1034768

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
            "parse_mode": "HTML"
        },
        timeout=20
    )

    response.raise_for_status()


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN غير موجود")

    if not CHAT_ID:
        raise ValueError("CHAT_ID غير موجود")

    g24, g22, g21, g18 = get_gold_prices()

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
