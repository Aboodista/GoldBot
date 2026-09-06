import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")


def fetch_gold_data():
    try:
        res = requests.get("https://data-asg.goldprice.org/dbXRates/SAR", timeout=10)
        data = res.json()

        item = data["items"][0]
        ounce_sar = item["xauPrice"]

        gram_24 = ounce_sar / 31.1035
        gram_22 = gram_24 * (22 / 24)
        gram_21 = gram_24 * (21 / 24)
        gram_18 = gram_24 * (18 / 24)

        chg_sar = item["chgXau"] * (3.75 / 31.1035)

        return {
            "g24": gram_24,
            "g22": gram_22,
            "g21": gram_21,
            "g18": gram_18,
            "chg": item["chgXau"],
            "chg_sar": chg_sar,
        }

    except Exception:
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    msg = (
        f"مرحباً بك يا {user} في بوت أسعار الذهب 🇸🇦🥇\n\n"
        "الأوامر المتاحة:\n"
        "• /gold - عرض أسعار الذهب الحالية 📊\n"
        "• /calc 50 - حساب قيمة الذهب لوزن معين 🧮\n\n"
        "البوت جاهز للعمل."
    )

    await update.message.reply_text(msg)


async def gold_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = fetch_gold_data()

    if not data:
        await update.message.reply_text(
            "تعذر جلب أسعار الذهب حالياً، حاول لاحقاً."
        )
        return

    msg = f"""
🇸🇦 **أسعار الذهب في السعودية** 🥇

• عيار 24: {data['g24']:.2f} ريال
• عيار 22: {data['g22']:.2f} ريال
• عيار 21: {data['g21']:.2f} ريال
• عيار 18: {data['g18']:.2f} ريال

📈 تغير الأوقية:
{data['chg']:.2f} USD

💰 التغير التقريبي للغرام:
{data['chg_sar']:+.2f} ريال
"""

    await update.message.reply_text(
        msg,
        parse_mode="Markdown"
    )


async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text(
                "اكتب الوزن بعد الأمر\nمثال:\n/calc 50"
            )
            return

        weight = float(context.args[0])

        data = fetch_gold_data()

        if not data:
            await update.message.reply_text(
                "تعذر جلب الأسعار حالياً."
            )
            return

        value21 = weight * data["g21"]
        value24 = weight * data["g24"]

        msg = f"""
🧮 **حاسبة الذهب**

الوزن: {weight} غرام

🥇 عيار 21:
{value21:,.2f} ريال

🥇 عيار 24:
{value24:,.2f} ريال
"""

        await update.message.reply_text(
            msg,
            parse_mode="Markdown"
        )

    except ValueError:
        await update.message.reply_text(
            "اكتب رقم صحيح، مثال:\n/calc 10"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold_price))
    app.add_handler(CommandHandler("calc", calculate))

    print("Gold Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
