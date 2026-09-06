import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def get_gold_prices():
    print("⏳ جاري جلب أسعار الذهب...")

    url = "https://data-asg.goldprice.org/dbXRates/SAR"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    print("📡 حالة موقع الذهب:", response.status_code)

    response.raise_for_status()

    data = response.json()

    if "items" not in data or not data["items"]:
        raise ValueError("❌ لم يتم العثور على بيانات الذهب")

    item = data["items"][0]

    ounce_price = float(item["xauPrice"])

    gram_24 = ounce_price / 31.1034768
    gram_22 = gram_24 * 22 / 24
    gram_21 = gram_24 * 21 / 24
    gram_18 = gram_24 * 18 / 24

    print("✅ تم جلب أسعار الذهب بنجاح")

    return gram_24, gram_22, gram_21, gram_18


def send_message(message):
    print("⏳ جاري إرسال الرسالة إلى تيليجرام...")

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

    print("📡 حالة Telegram:", response.status_code)
    print("📨 رد Telegram:", response.text)

    response.raise_for_status()

    result = response.json()

    if not result.get("ok"):
        raise ValueError(
            f"❌ Telegram رفض إرسال الرسالة: {result}"
        )

    print("✅ تم إرسال الرسالة بنجاح")


def main():
    print("🚀 بدء تشغيل بوت الذهب...")

    if not BOT_TOKEN:
        raise ValueError(
            "❌ BOT_TOKEN غير موجود. تأكد من إضافته في Environment Variables."
        )

    if not CHAT_ID:
        raise ValueError(
            "❌ CHAT_ID غير موجود. تأكد من إضافته في Environment Variables."
        )

    print("✅ BOT_TOKEN موجود")
    print("✅ CHAT_ID موجود")

    g24, g22, g21, g18 = get_gold_prices()

    now = datetime.now(
        ZoneInfo("Asia/Riyadh")
    )

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

    print("🎉 تم إرسال أسعار الذهب إلى القناة بنجاح!")


if __name__ == "__main__":
    main()
مهم: لا تغيّر هذين السطرين:
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
وفي إعدادات الاستضافة لازم تكون عندك:
BOT_TOKEN = توكن البوت
CHAT_ID = @GoldSaudiB
وبعدها شغّل البوت، وإذا ما اشتغل انسخ لي الـ Logs اللي تظهر لك وأنا أحدد المشكلة مباشرة.
